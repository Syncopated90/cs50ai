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
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    if len(corpus[page]) == 0:
        return equal_dict(corpus, page)
    p_random_page = (1 - damping_factor) / len(corpus)
    #print(f"p_random: {p_random_page}")
    new_dict = dict()
    for key in corpus[page]:
      new_dict.update({key : ((damping_factor / len(corpus[page])) + p_random_page)})
    for key in corpus:
        if key not in new_dict:
            new_dict.update({key: p_random_page})
    

    return new_dict

def equal_dict(corpus, page):
    new_dict = {page: None}
    for key in corpus:
      new_dict.update({key : None})
    for key in new_dict:
      new_dict[key] = 1 / len(new_dict)
    return new_dict



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilities_dict = dict()
    for key in corpus:
      probabilities_dict.update({key: 0})
    sample_page = random.choice(list(corpus.keys()))
    print(f"first sample page: {sample_page}")
    probabilities_dict[sample_page] += 1
    for number in range(1, n):
      markov_dict = transition_model(corpus, sample_page, damping_factor)
      #print(f"{markov_dict}")
      sample_page = random.choices(list(markov_dict.keys()), list(markov_dict.values()))[0]
      #print(f"sampled page: {sample_page}")
      probabilities_dict[sample_page] += 1
    for key in probabilities_dict:
        probabilities_dict[key] = probabilities_dict[key] / n
    return probabilities_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = dict()
    for key in corpus:
        pagerank_dict[key] = 1 / len(corpus)
    keep_iterating = True
    while keep_iterating:
    #for _ in range(0,1):
      keep_iterating = False
      for page in corpus:
        old_pagerank = pagerank_dict[page]
        #print(f"pr: {pagerank_dict[page]}")
        pagerank = 0
        for other_page in corpus:
           length = len(corpus[other_page])
           if length == 0:
              length = len(corpus)
              pagerank += (pagerank_dict[other_page] / length)
              continue
           if other_page == page:
              continue
           if page in corpus[other_page]:
            pagerank += (pagerank_dict[other_page] / length)
           #print(f"pr in this loop: {pagerank_dict[other_page] / len(corpus[other_page])}")
        #print(f"pagerank_dict: {pagerank_dict[page]}")
        #print(f"pr after for loop: {pagerank}")
        pagerank_dict[page] = (damping_factor * pagerank)
        #print(f"pr after for loop with damping factor: {pagerank * damping_factor}")
        pagerank_dict[page] += ((1 - damping_factor) / len(corpus))
        #print(f"{page}: {pagerank_dict[page]}")
        if old_pagerank - pagerank_dict[page] < -0.00001 or old_pagerank - pagerank_dict[page] > 0.00001:
          keep_iterating = True
    return pagerank_dict
if __name__ == "__main__":
    main()
