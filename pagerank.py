import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(" ")
    print("***************************************************")
    print(" ")
    print("Analysis for web page:")
    print(sys.argv[1])
    print(" ")
    print("***************************************************")
    print(" ")
    print(f"PageRank Results from Sampling (n = {SAMPLES})")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print(" ")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    print(" ")
    print("***************************************************")
    print(" ")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob = dict()
    pages = 0
    for entry in corpus:
        pages += 1
    #calculates probability that we randomly go to any page
    for entry in corpus:
        prob[entry] = (1-damping_factor)/pages
    # calculates probability that we go to a random link on the page
    for entry in corpus[page]:
       prob[entry] = prob[entry] + damping_factor/len(corpus[page])
    return prob






def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # creates a pagerank dictionary for each page in the file and initializes the times it was visited
    pagerank = dict()
    for entry in corpus:
        pagerank[entry] = 0
    # run a loop that calls the transition model to find the probability of the next page to be navigated to.
    #execute this loop n times and adjust the page rank to amount of times visited divided by n
    count = 0
    page = random.choice(list(corpus.keys()))
    #loop through n times and adjust the page rank
    while count < n:
        count += 1
        pagerank[page] += 1
        #generate random number that will be used to select a spot in the probability
        choice  = random.random()
        #get probability table
        prob = transition_model(corpus, page, damping_factor)

        # find next page to select
        probTotal = 0
        for item in prob:
            probTotal += prob[item]
            if choice <= probTotal:
                page = item
                break





    # change scale of probability so they sum to 1
    for page in pagerank:
        pagerank[page] = pagerank[page] / n


    '''
    print("probability ")
    for item in prob:
        print(item)
        print(prob[item])
    print(" ")
    '''




    return pagerank
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print(" ")
    print("Running iterate page rank func")
    # creates a pagerank dictionary for each page in the file and initializes the times it was visited
    pagerank = dict()
    for entry in corpus:
        pagerank[entry] = 1/len(corpus)
    n = 10000

    #calculate new page rank for each page in corpus
    terminate = True
    count = 0
    while terminate:
        terminate = False
        for entry in corpus:
            #calculate probabilty for an entry
            #first find the sum of PR(i)/numlinks(i) for each page that links to entry
            sum = 0
            links = 0
            for page in corpus:
                for link in corpus[page]:
                    if link == entry:
                        # if a link is found, caluclate the PR(i)/NumLinks(i) and add to sum
                        sum = sum + pagerank[page]/len(corpus[page])
                        links += 1
            if links == 0:
                sum = sum + pagerank[entry]/len(corpus)
            pagerank[entry] = (1-damping_factor)/len(corpus) + damping_factor*sum
        count += 1
        #scale values so they are between 1
        factor = 0
        for item in pagerank.values():
            factor += item
        #check for termination condition. if
        for item in pagerank:
            prev = pagerank[item]
            pagerank[item] = pagerank[item] / factor
            if abs(pagerank[item]-prev) < 0.001:
                terminate = True
        count += 1
    return pagerank


if __name__ == "__main__":
    main()
