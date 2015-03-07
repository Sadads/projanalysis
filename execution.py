# -*- coding: utf-8 -*-
"""
Execution file for ProjAnalysis
Version 1.0
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

from projanalysis import ProjAnalysis

if __name__ == "__main__":
    pairs=[
        ["WikiProject Star Trek", "WikiProject Star Trek"],
        ["WikiProject Christianity", "WikiProject Christianity"],
        ["WikiProject Latin music", "WikiProject Latin music"],
        ["WikiProject Women writers", "WikiProject Women writers"],
        ["WikiProject Cosmology", "WikiProject Cosmology"],
        ["WikiProject Microsoft", "WikiProject Microsoft"],
        ["WikiProject Microsoft Windows", "WikiProject Microsoft Windows"],
        ["WikiProject Beetles", "WikiProject Beetles"],
        ["WikiProject Animals", "WikiProject Animals"],
        ["WikiProject Biology", "WikiProject Biology"],
        ["WikiProject Björk", "WikiProject Björk"],
        ["WikiProject Buddhism", "WikiProject Buddhism"],
        ["WikiProject Cannabis", "WikiProject Cannabis"],
        ["WikiProject Cognitive science", "WikiProject Cognitive science"],
        ["WikiProject Cycling", "WikiProject Cycling"],
        ["WikiProject Dance", "WikiProject Dance"],
        ["WikiProject Disability", "WikiProject Disability"],
        ["WikiProject Eurovision", "WikiProject Eurovision"],
        ["WikiProject Evolutionary biology", "WikiProject Evolutionary biology"],
        ["WikiProject Food and drink", "WikiProject Food and drink"],
        ["WikiProject G.I. Joe", "WikiProject G.I. Joe"],
        ["WikiProject Ghana", "WikiProject Ghana"],
        ["WikiProject History", "WikiProject History"],
        ["WikiProject Human rights", "WikiProject Human rights"],
        ["WikiProject Islam", "WikiProject Islam"],
        ["WikiProject Linguistics", "WikiProject Linguistics"],
        ["WikiProject Lucknow", "WikiProject Lucknow"],
        ["WikiProject Mesoamerica", "WikiProject Mesoamerica"],
        ["WikiProject Nonviolence", "WikiProject Nonviolence"],
        ["WikiProject Open Access", "WikiProject Open Access"],
        ["WikiProject Physiology", "WikiProject Physiology"],
        ["WikiProject Pop music", "WikiProject Pop music"],
        ["WikiProject Protected areas", "WikiProject Protected areas"],
        ["WikiProject Psychology", "WikiProject Psychology"],
        ["WikiProject Religion", "WikiProject Religion"],
        ["WikiProject Rufus Wainwright", "WikiProject Rufus Wainwright"],
        ["WikiProject Sanitation", "WikiProject Sanitation"],
        ["WikiProject Schools", "WikiProject Schools"],
        ["WikiProject Science", "WikiProject Science"],
        ["WikiProject Streetcars", "WikiProject Streetcars"],
        ["WikiProject Tree of Life", "WikiProject Tree of Life"],
        ["WikiProject Wine", "WikiProject Wine"],
        ["WikiProject Hampshire", "WikiProject Hampshire"],
        ["WikiProject Worcestershire", "WikiProject Worcestershire"],                 # ^ signed up for pilot testing
        ["WikiProject Ancient Egypt", "WikiProject Ancient Egypt"],                              # v did not sign up for pilot testing
        ["WikiProject Pharmacology", "WikiProject Pharmacology"],
        ["WikiProject Opera", "WikiProject Opera"],
        ["WikiProject Video games", "WikiProject Video games"],
        ["WikiProject South Park", "WikiProject South Park"],
        ["WikiProject Dogs", "WikiProject Dogs"],
        ["WikiProject Iowa", "WikiProject Iowa"],
        ["WikiProject Military History", "WikiProject Military history"],
        ["WikiProject Molecular and Cellular Biology", "WikiProject Molecular and Cellular Biology"],
        ["WikiProject Pornography", "WikiProject Pornography"],
        ["WikiProject Bivalves", "WikiProject Bivalves"],
        ["WikiProject Gastropods", "WikiProject Gastropods"],
        ["WikiProject Lebanon", "WikiProject Lebanon"],
        ["WikiProject Albums", "WikiProject Albums"],
        ["WikiProject Film", "WikiProject Film"],
        ["WikiProject Football", "WikiProject Football"]
    ]
    
    # Taking out: WikiProject Guatemala, WikiProject United States presidential elections, WikiProject Louisville
    # Need to develop alternative process using WikiProject category tree
    
    print("Generating list of bots...")
        
    botqueryparams = {
        'list': 'allusers',
        'augroup': 'bot',
        'aulimit': 'max',
        'continue': ''
    }
        
    botquery = ProjAnalysis.mwquery(botqueryparams)
        
    bots = []
    for bot in botquery['query']['allusers']:
        bots.append(bot['name'])
        
    while 'continue' in botquery:
        botqueryparams['aucontinue'] = query['continue']['aucontinue']
        botquery = ProjAnalysis.mwquery(botqueryparams)
        for bot in botquery['query']['allusers']:
            bots.append(bot['name'])
        
    print("Counted " + str(len(bots)) + " bots.")
    
    for pair in pairs:
        proj = pair[0]
        bnr = pair[0]
        
        print("Now working on... " + proj)
        r = ProjAnalysis.analyze(proj, bnr, bots)
    