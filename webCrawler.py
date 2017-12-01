import urllib2  # used to open URLS
import sys
import string


def get_new_links_on_page(page, prev_links):
    try:
        page_response = urllib2.urlopen(page)
        html_element = page_response.read()
    except:
        print "\n-----------------------------------------------------------------------------------------"
        print " * WOOF! There was an error returning your URL - Please enter another URL into Poodle *"
        print "-----------------------------------------------------------------------------------------\n"
        crawler_main_func()

    links, pos, all_found, page_links = [], 0, False, []

    while not all_found:
        a_tag = html_element.find("<a href=", pos)
        if a_tag > -1:
            href = html_element.find('"', a_tag + 1)
            end_href = html_element.find('"', href + 1)
            url = html_element[href + 1:end_href]

            if url[:8] == "https://" or url[:7] == "http://":
                if url[-1] == "/":
                    url = url[:-1]
                page_links.append(url)

                if url not in links and url not in prev_links:
                    links.append(url)
                    # print url
            close_tag = html_element.find("</a>", a_tag)
            pos = close_tag + 1

        else:
            all_found = True
    return links, page_links


def crawler_main_func():

    MAX_CRAWL_DEPTH = 5
    crawl_count = []
    urls_crawled = {}
    user_prompt = raw_input(" Please provide a seed URL (enter -close to exit) >> ")
    if user_prompt == "-close":
        sys.exit()
    elif user_prompt[:8] == "https://" or user_prompt[:7] == "http://":  # check if URL is http or https
        if user_prompt[-1] == "/":  # remove forward slash from the end
            user_prompt = user_prompt[:-1]
        # removes whitespace and punctuation from user entered string
        #  see: https://www.dotnetperls.com/punctuation-python
        user_prompt = user_prompt.strip(string.punctuation)
        user_prompt = user_prompt.lower()  # converts to lowercase

        # print user_prompt

        url_to_crawl = [user_prompt]
        while url_to_crawl and len(crawl_count) < MAX_CRAWL_DEPTH:
            unique_crawled_urls = []
            url = url_to_crawl.pop()
            crawl_count.append(url)

            # print "CRAWL COUNT ======"
            # print len(crawl_count)

            new_links = get_new_links_on_page(url, urls_crawled)

            if url not in unique_crawled_urls:
                unique_crawled_urls.append(url)

                # print "UNIQUE URLS ====="
            url_to_crawl = list(set(url_to_crawl) | set(new_links[0]))

            urls_crawled[url] = new_links[1]

            for url in unique_crawled_urls:
                print url

        return urls_crawled
    else:
        print "\n------------------------------------------------------------------------------------------"
        print " * WOOF! URL must start with http:// or https:// - Please enter another URL into Poodle *"
        print "------------------------------------------------------------------------------------------\n"

        crawler_main_func()

