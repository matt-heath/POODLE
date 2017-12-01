import urllib2
import string


def get_page_text(url):
    page_response = urllib2.urlopen(url)
    html_element = page_response.read()

    text_on_page, words_on_page = "", []
    html_element = html_element[html_element.find("<body") + 5:html_element.find("</body>")]

    start_script = html_element.find("<script")
    while start_script > -1:
        end_script = html_element.find("</script>")
        html_element = html_element[:start_script ] + html_element[ end_script + 9:]
        start_script = html_element.find("<script")

    ignore = []
    fin = open("ignoreList.txt", "r")
    for word in fin:
        ignore.append(word.strip())
    fin.close()

    finished = False
    while not finished:
        next_close_tag = html_element.find(">")
        next_open_tag = html_element.find("<")
        if next_open_tag > -1:
            content = " ".join(html_element[next_close_tag + 1:next_open_tag].strip().split())
            text_on_page = text_on_page + " " + content
            html_element = html_element[next_open_tag + 1:]
        else:
            finished = True

    for word in text_on_page.split():
        word = word.lower()
        word = word.strip(string.punctuation)
        if word[0].isalnum() and not word in ignore:
            if not word in words_on_page:
                words_on_page.append(word)
    # print words_on_page
    return words_on_page


def add_to_scraped_dictionary(scraped_dictionary, page_words, url):
        if page_words in scraped_dictionary:
            scraped_dictionary[page_words].append(url)
            return
        scraped_dictionary[page_words] = [url]


def url_page_scraper_main_func(graph):
    scraped_dictionary = {}
    for url in graph:
        page_words = get_page_text(url)

        for word in page_words:
            add_to_scraped_dictionary(scraped_dictionary, word, url)

    return scraped_dictionary
