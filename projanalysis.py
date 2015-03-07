# -*- coding: utf-8 -*-
"""
ProjAnalysis -- performs analysis of a WikiProject. Use sparingly.
Version 1.2
Copyright (C) 2015 James Hare
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import sys
import json
import mw # https://github.com/legoktm/supersimplemediawiki
import pymysql

class ProjAnalysis:
    def mwquery(inputparams):
        """Constructs a MediaWiki query. Uses Legoktm Magic."""
        
        enwp = mw.Wiki('https://en.wikipedia.org/w/api.php')
        enwp.login()
        
        params = {'action': 'query'} # Initializing with parameters that will be in every query
        params.update(inputparams) # Adding in inputed parameters
        
        data = enwp.request(params)
        
        return data

    def dbquery(sqlquery):
        """Constructs a MySQL query to the Tool Labs database replica."""
        
        conn = pymysql.connect(host='enwiki.labsdb', port=3306, db='enwiki_p', read_default_file='~/.my.cnf')
        cur = conn.cursor()
        cur.execute(sqlquery)
        data = []
        for row in cur:
            data.append(row[0])
        return data
    
    def getsubpages(prefix, namespace):
        """Gets subpages of a given page through MediaWiki API. The API limits to 500 results per query with a continue option. This iterates through until it's done."""
        
        functionparams = {
        	'list': 'allpages',
        	'apnamespace': namespace,
        	'apprefix': prefix + '/',
        	'aplimit': 'max',
        	'continue': ''
        }
        
        output = []
        query = ProjAnalysis.mwquery(functionparams)
        for x in query['query']['allpages']:
            output.append(x['pageid'])
        
        while 'continue' in query:
            functionparams['apcontinue'] = query['continue']['apcontinue']
            query = ProjAnalysis.mwquery(functionparams)
            for x in query['query']['allpages']:
                output.append(x['pageid'])
        
        return output
    
    def contributorfinder(title):
        """Prepares a list of contributors for *title* in a given date range. Includes duplicate usernames for each time they made an edit."""
        
        query = "select rev_user_text from revision_userindex where rev_page = " + str(title) + " and rev_timestamp > 20140228235959 and rev_timestamp < 20150301000000 and rev_user != 0 and rev_user_text != 'Harej';"
        
        usernames = ProjAnalysis.dbquery(query)
        
        output = []
        for username in usernames:
            output.append(username.decode('utf-8'))
        
        if len(usernames) == 0:
            return None
        else:
            return output
    
    def userstats(completelist, bots):
        """Removes bot list of usernames and gives edit frequency information using the list that has not been de-duped."""
        
        uniques = list(set(completelist)) # De-duplication
        humans = list(set(uniques) - set(bots)) # Removing bots
            
        # Measuring frequency
        
        output = {}
        for human in humans:
            freq = completelist.count(human)
            output[human] = freq
        
        return output
    
    def articlesinscope(template):
        """Comes up with the list of pages transcluding *template* and corresponding talk pages."""
        
        functionparams = {
            'prop': 'transcludedin',
            'tilimit': 'max',
            'titles': 'Template:' + template,
            'continue': ''
        }
        
        query = ProjAnalysis.mwquery(functionparams)
        
        transcludeslist = list(query['query']['pages'].values())[0]['transcludedin']
        
        talks = []
        for transclude in transcludeslist:
            talks.append(transclude['pageid'])
            
        while 'continue' in query:
            functionparams['ticontinue'] = query['continue']['ticontinue']
            query = ProjAnalysis.mwquery(functionparams)
            transcludeslist = list(query['query']['pages'].values())[0]['transcludedin']
            for transclude in transcludeslist:
                talks.append(transclude['pageid'])
        
        # That list produces talk pages. We also want the non-talk pages.
        
        nontalks = []
        for talk in talks:
            query = "Select p1.page_id from page p1 inner join page p2 on p1.page_namespace = p2.page_namespace - 1 and p1.page_title = p2.page_title where p2.page_id = " + str(talk) + ";"
            nontalk = ProjAnalysis.dbquery(query)
            if nontalk:
                nontalks.append(nontalk[0])
        
        output = talks + nontalks
        
        return output
        

    def analyze(project, banner, bots):
        """The master class. Invokes all the other classes."""
        
        # Generate list of WikiProject subpages
        
        print("Generating list of WikiProject subpages...")
        allpages = ProjAnalysis.getsubpages(project, 4) # "Wikipedia:" namespace
        alltalkpages = ProjAnalysis.getsubpages(project, 5) # "Wikipedia talk:" namespace
        
        # We need page IDs for our main WikiProject page and talk page. Note that this returns a one-entry list.
        root_page = ProjAnalysis.dbquery("select page_id from page where page_title='" + project.replace(" ", "_") + "' and page_namespace=4;")
        root_talk = ProjAnalysis.dbquery("select page_id from page where page_title='" + project.replace(" ", "_") + "' and page_namespace=5;")
        
        projectpages = [root_page[0], root_talk[0]] # Initializing list with main project page and its talk page
        projectpages += allpages
        projectpages += alltalkpages
        
        # We now have our list of pages.
        
        print("Generating list of WikiProject-space contributors...")
        projectcontributors = []
        for page in projectpages:
            listoutput = ProjAnalysis.contributorfinder(page)
            if listoutput is not None: # The above function returns None if there are no contributors in the given time span.
                for x in listoutput:
                    projectcontributors.append(x)
        
        print("Counting edits per user...")
        output_project = ProjAnalysis.userstats(projectcontributors, bots) # Note that *projectcontributors* contains duplicates.
        
        # At this point, we have a list of dictionaries of users and the number of times they edited the project's space.
        # Now, to do the same with the pages in that project's scope, as determined through tagging.
        
        print("Generating list of pages in WikiProject's scope...")
        allarticles = ProjAnalysis.articlesinscope(banner) # Generates list of pages tagged by a WikiProject including talk page
        projectscope = list(set(allarticles) - set(projectpages)) # Removes WikiProject space pages from list of tagged articles
        
        scopecontributors = []
        for page in projectscope:
            print("Fetching edit history of page ID " + str(page) + "...")
            listyield = ProjAnalysis.contributorfinder(page)
            if listyield is not None:
                for x in listyield:
                    scopecontributors.append(x)
        
        print("Counting users per edit...")
        output_scope = ProjAnalysis.userstats(scopecontributors, bots)
        
        # Preparing CSV file
        print("Preparing report on " + project + "...")
        report = "Username,Project Edits,Scope Edits,Total\n" # Headers
        
        
        usernames_project = list(output_project.keys())
        usernames_scope = list(output_scope.keys())
        usernames = usernames_project + list(set(usernames_scope) - set(usernames_project)) # Combining lists for CSV
        
        for username in usernames:
            if username not in usernames_project:
                column2 = 0 # No edits to the project space
            else:
                column2 = output_project[username]
            if username not in usernames_scope:
                column3 = 0 # No edits to the project scope
            else:
                column3 = output_scope[username]
            lineitem = username + "," + str(column2) + "," + str(column3) + "," + str(column2 + column3) + "\n"
            report += lineitem
        
        total_project = sum(list(output_project.values()))
        total_scope = sum(list(output_scope.values()))
        report += "*TOTAL*," + str(total_project) + "," + str(total_scope) + "," + str(total_project + total_scope) + "\n"
        
        print("Saving report...")
        filename = project + ".csv"
        save = open(filename, "w")
        save.write(report)
        save.close()