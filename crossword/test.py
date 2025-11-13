from crossword import*
from generate import *
import random

def main():
  
  crossword = Crossword("data/structure0.txt", "data/words0.txt")
  #crossword = Crossword("data/structure2.txt", "data/words2.txt")
  crossword = Crossword("data/structure0.txt", "data/words2.txt")
  creator = CrosswordCreator(crossword)
  creator.enforce_node_consistency()
  print_crossword(creator)
  first_var = Variable(1, 4, "down", 4)
  #second_var = Variable(4, 1, "across", 4)
  #creator.domains[first_var] = {'XXXX'}
  #print(first_var)
  #print(second_var)
  #x: (1, 4) down : 4: {'FOUR', 'NINE', 'FIVE'}, y: (4, 1) across : 4: {'FOUR', 'NINE', 'FIVE'}
  """
  if creator.revise(first_var, second_var):
    print("change made")
    print(f"{first_var}: {creator.domains[first_var]}")
    """
  #print(f"{first_var}: {creator.domains[first_var]}")
  if not creator.ac3():
    print("ac3 failed")
    print_crossword(creator)
  else:
    print("ac3 test succeded")
    print_crossword(creator)
  """
  print(f"assignment complete? {creator.assignment_complete(creator.domains)}")
  
  make_words_unique(creator)
  
  print_crossword(creator)
  print(f"consistent assignment? {creator.consistent(creator.domains)}")
  """
  #creator.order_domain_values(first_var, [])
  print(f"assigned: {first_var} an unassigned variable: {creator.select_unassigned_variable([first_var])}")

def make_words_unique(creator):
    for variable in creator.domains:
        creator.domains[variable] = random.choice(list(creator.domains[variable]))
def print_crossword(creator):
  keys = list(creator.domains)
  values = list(creator.domains.values())
  print("print crossword")
  for number in range(0,4):
    print(f"{keys[number]}: {values[number]}")

if __name__ == "__main__":
  main()