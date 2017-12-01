import pickle
import re
import sys
import os
import pprint
import string
from operator import itemgetter

# import other created files 'webCrawler, urlPageScraper, getPageRank
import webCrawler
import urlPageScraper
import getPageRank

# 'pretty prints' the page ranks when the user selects the '-print' option,
# see: https://docs.python.org/2/library/pprint.html
pp = pprint.PrettyPrinter(depth=6)

poodle_dictionary = {}  # Gives an empty poodle dictionary to be updated throughout the file
# sets poodle_database_built to a default of false - gets updated to true when the database is built later in the file
poodle_database_built = False


# help_Menu_Options_func - This function creates an empty dictionary and then adds values based on the status of
# 'poodle_database_built'. If false, the user will be required to -build, -restore or close and if true,
# the user will have access to all options within the help menu.


def help_menu_options_func():
    help_menu_options = {}  # gives an empty dictionary to be used when assigning relevant help menu options

    while True:
        print "\n WOOF! What can Poodle do for you?\n "
        print " -build Creates the poodle database \n -restore Retrieve dump"
        if poodle_database_built:
            print " -dump Save database "
            if os.path.isfile('poodle.txt'):
                print" -delete Delete current database "
            print" -print Print database \n -search Search the database"
        print " -close Exit POODLE \n"

        user_input = raw_input(" Selected Menu Option: ")
        user_input = user_input.lower()  # takes the user input and converts it to lower case.
        user_input = user_input.strip()  # removes whitespace from the entered user string
        # see: https://www.tutorialspoint.com/python/string_strip.htm

        if not poodle_database_built:  # checks to see if poodle__database_built is false and if it is,
            # returns relevant user options along with their functions created below.
            help_menu_options['-build'] = poodle_build
            help_menu_options['-restore'] = poodle_restore
            help_menu_options['-close'] = sys.exit
        else:
            # if poodle_database_built is true, the user gets access to all available menu functionality within poodle.
            help_menu_options['-build'] = poodle_build
            help_menu_options['-restore'] = poodle_restore
            help_menu_options['-search'] = poodle_search
            help_menu_options['-dump'] = poodle_dump
            if os.path.isfile('poodle.txt'):
                help_menu_options['-delete'] = poodle_delete
            help_menu_options['-print'] = poodle_print
            help_menu_options['-close'] = sys.exit  # quits execution of the python program
            # see: https://docs.python.org/2/library/sys.html#sys.exit

        # checks if the string input by the user exists in the 'help_menu_options' dictionary
        # and 'breaks' the while loop if it is.
        if user_input in help_menu_options:
            break
        else:
            print " ---------------------------------------------------------------------------"
            print "  * WOOF! Invalid option entered. Please choose an option from the list. *"
            print " ---------------------------------------------------------------------------"

    # takes the user input and goes tries to find the entered values
    # within the hel_menu_options dictionary, returning the associated function.
    help_menu_options[user_input]()


def poodle_build():
    graph = webCrawler.crawler_main_func()
    index = urlPageScraper.url_page_scraper_main_func(graph)
    # print index
    ranks = getPageRank.get_page_ranks(graph)

    # add all data to poodle dictionary
    poodle_dictionary['graph'] = graph
    poodle_dictionary['index'] = index
    poodle_dictionary['ranks'] = ranks

    global poodle_database_built
    poodle_database_built = True  # change database built to True
    print "\n-------------------------------------------"
    print " * WOOF! Poodle database has been built! *"
    print "-------------------------------------------\n"

    help_menu_options_func()
    return graph, index, ranks


def poodle_search():
    global search_result, rank
    search_result = []
    rank = []
    index = poodle_dictionary['index']
    ranks = poodle_dictionary['ranks']

    if not poodle_database_built:
        print "\n-----------------------------------------------------------------------------------------------"
        print " * WOOF! Poodle database has not yet been built - Use -build to create a searchable database. *"
        print "-----------------------------------------------------------------------------------------------\n"
    else:
        while True:
            poodle_search_criteria = raw_input("\n Enter a search term (enter -close to exit) >> ")
            poodle_search_criteria = poodle_search_criteria.lower()

            # print poodle_search_criteria

            if poodle_search_criteria == "-close":
                help_menu_options_func()
            else:
                # removes whitespace and punctuation from user entered string
                #  see: https://www.dotnetperls.com/punctuation-python
                poodle_search_criteria = poodle_search_criteria.strip(string.punctuation)
                poodle_search_list = re.findall(r"[\w']+", poodle_search_criteria.lower())

                # print "SEARCH LIST: ------------"
                # print poodle_search_list

                for x in poodle_search_list:
                    # try:
                    if x in index:
                        search_result.extend(index[x])
                    # print search_result
                    # except:
                    #     print "\n WOOF! No results found in the poodle database - Please search again! "
                    #     poodle_search()

                # print "\nSEARCH RESULT: ------- "
                # print search_result

                if search_result == "":
                    print "\n--------------------------------------------------------------------------"
                    print "* WOOF! No results found in the poodle database - Please search again! *"
                    print "--------------------------------------------------------------------------\n"
                else:
                    results = {}
                    for res in search_result:
                        page_rank = ranks[res]

                        # print "\nRANK PRINT ===="
                        # print page_rank
                        results[res] = page_rank

                    query_return = results

                    # print"QUERY RETURN ======="
                    # print query_return

                    # print query_return
                    no_of_results = len(query_return)
                    if search_result is None or no_of_results == 0:
                        print "\n--------------------------------------------------------------------------"
                        print " * WOOF! No results found in the poodle database - Please search again! *"
                        print "--------------------------------------------------------------------------\n"
                    else:
                        if no_of_results == 1:
                            print "\nShowing the " + str(no_of_results) + " result found"
                        else:
                            print "\nShowing the " + str(no_of_results) + " results found"
                        for key, value in sorted(query_return.items(), key=itemgetter(1), reverse=True):
                            print(key, value)

            # search_result = []
            # rank = []

            poodle_search()


def poodle_dump():
    # open and write to the poodle.txt file, dumping the created 'poodle_dictionary' into the file.
    fout = open("poodle.txt", "w")
    pickle.dump(poodle_dictionary, fout)
    fout.close()

    print "\n -------------------------------"
    print "  * WOOF! Poodle data buried. *"
    print " -------------------------------\n"
    help_menu_options_func()


def poodle_restore():
    global poodle_dictionary
    if os.path.exists("poodle.txt"):
        fin = open("poodle.txt", "r")
        poodle_dictionary = pickle.load(fin)
        fin.close()

        global poodle_database_built
        poodle_database_built = True

        print "\n-----------------------------------------------"
        print " * WOOF! Poodle database has been restored. * "
        print "-----------------------------------------------\n"
        print " Dictionary found: \n"
        print poodle_dictionary
    else:
        print "\n----------------------------------------------------------------------------------------"
        print " * Poodle database has not yet been built. Use -build to create a searchable database. * "
        print "----------------------------------------------------------------------------------------\n"

    help_menu_options_func()


def poodle_delete():
    if not os.path.isfile('poodle.txt'):
        print "\n -------------------------------------------------------"
        print "  * WOOF! No poodle database file available to delete * "
        print " -------------------------------------------------------\n"
        help_menu_options_func()
    else:
        os.remove('poodle.txt')

        print "\n -----------------------------------------"
        print "  * WOOF! Poodle database file deleted! * "
        print " -----------------------------------------\n"

        global poodle_database_built
        poodle_database_built = False

        help_menu_options_func()


def poodle_print():
    # print poodle graph from poodle_dictionary
    print "\n------------"
    print " PAGE GRAPH "
    print "------------\n"
    print poodle_dictionary["graph"]

    # print poodle index from poodle_dictionary
    print "\n------------"
    print " PAGE INDEX "
    print "------------\n"
    pp.pprint(poodle_dictionary["index"])

    # print poodle page ranks from poodle_dictionary
    print "\n------------"
    print " PAGE RANKS "
    print "------------\n"
    # pp.pprint(poodle_dictionary["ranks"])

    # sorts the page ranks by ascending order.
    # See: https://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
    for key, value in sorted(poodle_dictionary["ranks"].iteritems(), key=lambda (k,v): (v,k)):
        print "%s" % [key, value]

    help_menu_options_func()


help_menu_options_func()
