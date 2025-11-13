import sys
import random

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            new_values = set()
            for value in self.domains[variable]:
                if len(value) == variable.length:
                    new_values.add(value)
            self.domains[variable] = new_values
        #for variable in self.domains:
        #    print(f"Variable: {variable}\nDomain: {self.domains[variable]}")

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #print(f"variable x: {x}, values for x: {self.domains[x]}\nvariable y: {y}, values for y: {self.domains[y]}")
        #for overlap in self.crossword.overlaps:
            #print(f"{overlap}") #: {self.crossword.overlaps[overlap]}
        if self.crossword.overlaps[(x,y)] is None:
          #print(f"no overlap between {x} and {y}")
          return False
        else:
            (i, j) = self.crossword.overlaps[(x,y)]
            #print(f"overlap: {(i, j)}")
            #print(f"self domains[x]: {self.domains[x]}")
            new_words = set()
            change_made = False
            for value in self.domains[x]:
              for word in self.domains[y]:
                if value[i] == word[j]:
                    new_words.add(value)
                    #print(f"intersection x val: {value[i]}, y val: {word[j]}")
            if not self.compare_word_lists(self.domains[x], new_words):
              self.domains[x] = new_words
              change_made = True
            return change_made
        
    def compare_word_lists(self, list1, list2):
        equal = True
        for word in list1:
            if word not in list2:
                equal = False
        #if not equal:
          #print("lists are not eual")
          #print(list1)
          #print(list2)
        return equal

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        if arcs is None:
            arcs = self.create_all_arcs()
        change_made = True
        while change_made:
            change_made = False
            for item in arcs:
                if self.revise(item[0], item[1]):
                    #print(f"x: {item[0]}: {self.domains[item[0]]}, y: {item[1]}: {self.domains[item[1]]}")
                    change_made = True
        """
        print("finished list")
        for item in self.domains:
            print(f"{item}: {self.domains[item]}")
        """
        for item in self.domains:
            if self.domains[item] == set():
                return False
        return True
        
                
    def create_all_arcs(self):
        arcs = set()
        for variable in self.domains:
            for other_var in self.domains:
                if variable != other_var:
                    arcs.add((variable, other_var))
        return arcs
                    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        for key in assignment:
            #print(f"{assignment[key]}")
            if assignment[key] == set():
                complete = False
        return complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if not self.all_words_are_unique(assignment):
            return False
        for variable in assignment:
            if not self.check_length(variable, assignment[variable]):
                print("wrong length")
                return False
            if not self.check_conflicts(variable, assignment):
                print("conflict!")
                return False
        return True
    
    def all_words_are_unique(self, assignment):
        word_list = list()
        word_set = set()
        current_word_list = list(assignment.values())
        print(current_word_list)
        for word in current_word_list:
          word_list.append(word)
          word_set.add(word)
        print(f"word list: {word_list}")
        print(f"word set: {word_set}")
        if len(word_list) != len(word_set):
            return False
        return True
            
    def check_length(self, variable, word):
        if word == set():
            return False
        #print(variable.length)
        #print(words)
        if len(word) != variable.length:
            return False
        return True
    
    def check_conflicts(self, variable, assignment):
        for other_variable in assignment:
            if variable == other_variable:
                continue
            if self.crossword.overlaps[(variable, other_variable)] is None:
                continue
            else:
                (i, j) = self.crossword.overlaps[(variable, other_variable)]
                if assignment[variable][i] != assignment[other_variable][j]:
                    return False
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        values = list()
        #print(f"values: {values}")
        for word in self.domains[var]:
            values.append((word, self.count_ruled_out_values(var, word, assignment)))
        #print(f"values: {values}")
        #print(sorted(values, key = lambda count: count[1]))
        return sorted(values, key = lambda count: count[1])
    
    def count_ruled_out_values(self, var, word, assignment):
        neighbors = self.find_neighboring_vars_not_in_assignment(var, assignment)

        count = 0
        for variable in neighbors:
            (i, j) = self.crossword.overlaps[(var, variable)]
            for element in self.domains[variable]:
              if word[i] != element[j]:
                  count += 1
        #print(f"word: {word}, ruled out count: {count} in neighbors: {neighbors}")
        return count
        
            
    def find_neighboring_vars_not_in_assignment(self, variable, assignment):
        neighbors = list()
        for other_var in self.domains:
            if other_var == variable or self.crossword.overlaps[(variable, other_var)] == None:
                continue
            else:
                neighbors.append(other_var)
        #print("neighbors: ")
        #print(neighbors)
        return neighbors
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = []
        for var in self.domains:
            if var not in assignment:
                unassigned_variables.append((var, len(self.domains[var]), self.count_degree(var)))
        #unassigned_variables.append(("variable", 174, 2))
        #unassigned_variables.append(("variable", 174, 6))
        list.sort(unassigned_variables, key = lambda element: (element[1], -element[2]))
        #list.sort(unassigned_variables, key = lambda element: element[2], reverse = True)
        #print(unassigned_variables)
        return unassigned_variables[0][0]
    def count_degree(self, var):
        count = 0
        for other_var in self.domains:
            if var == other_var or self.crossword.overlaps[var, other_var] == None:
                continue
            else:
                count += 1
        return count
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        unassigned_var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(unassigned_var, assignment):
            assignment[unassigned_var] = value
            result = self.backtrack(assignment)
            if result is not None:
                return result
            assignment.pop(unassigned_var, None)
            


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
