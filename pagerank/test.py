from pagerank import transition_model, equal_dict, sample_pagerank, iterate_pagerank
damping_factor = 0.85
corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
corpus2 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}, "4.html" : {}}

corpus = corpus
page = list(corpus.keys())[0]

def main():
  print(f"{corpus}")
  #for key in corpus:
    #print(f"{key}: {corpus[key]} length of value: {len(corpus[key])}")
  #print(f"length: {len(corpus)}")
  #print(f"(1 - 0.85) / 3: {(1-0.85) / 3:.2f}")
  #print(f"flattened dict: {equal_dict(corpus, page)}")
  """
  sample_dict = sample_pagerank(corpus, damping_factor, 1000)
  print(f"{transition_model(corpus, page, damping_factor)}")
  print(f"pagerank: {sample_dict}")
  print(f"pagerank keys as list: {list(sample_dict.keys())}")
  print(f"pagerank values as list: {list(sample_dict.values())}")
  print(f"sum of list: {sum(list(sample_dict.values()))}")
  """
  iter_pr = iterate_pagerank(corpus, damping_factor)
  print(f"iterable pagerank: {iter_pr}")
  print(f"sum of values: {sum(list(iter_pr.values()))}")

if __name__ == "__main__":
    main()