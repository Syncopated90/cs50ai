import nltk
import sys

from nltk import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP NP | NP VP NP VP | S Conj S | S Adv | S Conj VP NP
NP -> Det N | N | Adj N | P N | NP NP | Det Adj N | P Det Adj N | P Det N | NP NP NP
VP -> V | V P | V Adv | Adv V 
Adj -> Adj Adj 

"""
"""
9: V N P Det Adj N
10: N V Det Adj Adj Adj N P Det N P Det N : NP VP NP NP NP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    print(sentence)
    s = word_tokenize(sentence)
    word_list = []
    for word in s:
        if is_alpha_numeric(word):
          word_list.append(str.lower(word))
    return word_list

def is_alpha_numeric(word):
    for char in word:
        if char.isalpha():
            return True
    return False

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    for s in tree.subtrees(lambda t: t.label() == 'NP'):
        if is_np_chunk(s):
          np_chunks.append(s)
     #     print(s)
    #for np in np_chunks:
        #print(np)
    return np_chunks

def is_np_chunk(tree):
    #print(f"Entry :{tree.label()} height: {tree.height()}")
    if tree.label() != 'NP':
        return False
    for s in tree.subtrees():
        if s == tree:
            continue
        if s.label() == 'NP':
            #print(f"second if :")
            #print(s)
            #for ss in s.subtrees():
                #print("subtrees: ")
                #print(ss)
            return False
    return True

if __name__ == "__main__":
    main()
