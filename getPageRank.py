# function to return the page ranks for the scraped links - code from
def get_page_ranks(graph):
    default = 0.85
    num_of_loops = 10
    page_ranks = {}
    num_of_pages = len(graph)

    for page in graph:
        page_ranks[page] = 1.0 / num_of_pages

    for i in range(0, num_of_loops):
        updated_ranks = {}
        for page in graph:
            updated_rank = (1 - default) / num_of_pages
            for node in graph:
                if page in graph[node]:
                    updated_rank = updated_rank + default * (page_ranks[node] / len(graph[node]))
            updated_ranks[page] = updated_rank
        page_ranks = updated_ranks
    return page_ranks
