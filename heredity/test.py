from heredity import joint_probability 

def main():
  people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
  }
  p = joint_probability(people, {"Harry"}, {"James"}, {"James"})
  print(f"joint prob: {p}")
if __name__ == "__main__":
  main()