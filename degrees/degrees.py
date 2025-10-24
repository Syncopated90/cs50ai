import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path(source, target):
    start_node = Node(source, parent=None, action=None)
    frontier = StackFrontier()
    explored = set()
    frontier.add(start_node)
    target_found = False
    #if frontier.contains_state(person_id_for_name("tom hanks")):
        #print(f"tom hanks is here")
    while not target_found:
        if frontier.empty():
          return None
        node = frontier.remove()
        if getattr(node, 'state') == target:
          path = []
          #print(f"node state: {node.state} parent: {node.parent} action: {node.action}")
          while node.parent is not None:
              path = [(getattr(node, 'action'), getattr(node, 'state'))] + path
              node = getattr(node, 'parent')
          return path
        explored.add(getattr(node, 'state'))
        for neighbor in neighbors_for_person(getattr(node, 'state')):
          if neighbor[1] not in explored and not frontier.contains_state(neighbor[1]):
              frontier.add(Node(neighbor[1], node, neighbor[0]))
              #print(f"neighbor state: {neighbor[1]} neighbor action: {neighbor[0]}")
def old_shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    path = []
    node = Node(source, None, None)

    """test = set([Node(1, None, None),Node(2,None,None)])
    test.add(Node(1, None, None))
    for node in test:
      print(f"id: {getattr(node, "state")}, last id: {getattr(node, "parent")}, movie: {getattr(node, "action")}")
    if Node(3 , None, None) not in test:
        print(f"3 not in 1,2")
    if Node(1 , None, None) in test:
        print(f"1 in 1,2")"""

    frontier = StackFrontier()
    explored = set()
    frontier.add(node)
    #explored.add(node)
    target_found = False
    while not target_found:
      node = frontier.remove()
      #print(f"current node id:{getattr(node, "state")}")
      #print(f"type: {type(getattr(node, "state"))}")
      neighbors = neighbors_for_person(getattr(node, "state"))
      for neighbor in neighbors:
        #print(f"current neighbor id: {neighbor[1]}")
        #print(f"type: {type(neighbor[1])}")
        if neighbor[1] == getattr(node, "state"):
          print(f"{neighbor[1]} and {getattr(node, "state")} are the same")
          continue
        print(f"Source's neighbor: {neighbor}")
        if neighbor[1] == target:
          path.append(neighbor)
          target_found = True
          print(f"target found: {neighbor[1]}")
          break
        neighbor_node = Node(neighbor[1], getattr(node, "state"), neighbor[0])
        if not node_was_explored(neighbor_node, explored):
          neighbor_node = Node(neighbor[1], getattr(node, "state"), neighbor[0])
          frontier.add(neighbor_node)
          #for node in explored:
            #print(f"id: {getattr(node, "state")}, last id: {getattr(node, "parent")}, movie: {getattr(node, "action")}")
        explored.add(node)
      #print(f"{neighbors}")
    if len(path) == 0:
      return None
    else:
      return path#[("109830","102"),("95953","200")]
    
def node_was_explored(node, set):
    return (any(getattr(node, "state") == getattr(element, "state") for element in set)
    and any(getattr(node, "parent") == getattr(element, "parent") for element in set) and
    any(getattr(node, "action") == getattr(element, "action") for element in set))
def check_same_person(source, target):
    return source != target

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
