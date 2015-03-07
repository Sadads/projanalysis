# projanalysis
ProjAnalysis is an analysis tool for WikiProjects on the English Wikipedia. The tool will produce a CSV file listing each user,
the number of edits they've made to the project's space (i.e. the WikiProject page itself and its subpages), and the number of
edits they have made to pages that are in that WikiProject's scope. Currently the script is configured to run the analysis on
a one-year period beginning on March 1, 2014 and ending February 28, 2015.

ProjAnalysis comes in two parts: projanalysis.py, containing the ProjAnalysis class, and execution.py, which produces the list
of bots to exclude from the analysis and includes the list of WikiProjects to analyze.

If you want to analyze a WikiProject, you will need to edit the *pairs* dictionary in execution.py. Each entry in the dictionary
is in turn a dictionary with two items. The first item is the name of the WikiProject itself (the page title without the
"Wikipedia:" part) and the second part is the name of the WikiProject banner (without the "Template:" part). It turns out in
practice the two will have identical titles (for example, "Wikipedia:WikiProject Star Trek" and "Template:WikiProject Star
Trek"), but I coded it like this in case *for whatever reason* the two titles differ. Once you have configured execution.py with
your files, go ahead and run it. This is intended to be used in Python 3.

Current issue:

* The script's workflow assumes that each WikiProject has a dedicated WikiProject banner. This is not always the case! Some
  WikiProjects have consolidated their banners into banners of larger projects. For example, WikiProject District of Columbia
  is given a line on the template for the broader WikiProject United States. An alternative workflow will need to be developed
  that depends on the WikiProject assessment category tree, or something else that figures out the pages in the project scope.
* Originally, the script relied on the API exclusively. This created a huge bottleneck when loading thousands of pages. Now THAT   part is handled strictly by database querying, which is extremely fast. API is still used in parts, so we have something of a   hybrid solution going. At some point it should switch to being all database.
