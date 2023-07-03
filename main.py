# main.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Utilizes an adjacency list graph implementation as well as an API
# & source code scraper to create a topological sort of classes.
# A.K.A. an ordering of classes such that if taken in order,
# prerequisites will not be violated.

from query import prereq, valid_class, check_for_unlisted_prereqs
from graph import Graph


def _topological_sort(graph: 'Graph', nodes: list) -> None:
    """
    Outputs a topological sort by repeatedly removing nodes
    with 0 in-degree.

    Citation: Professor Michael Shindler, ICS-46
    """
    count = 1
    class_list = graph.getKeys()

    available = []
    for node in nodes:
        if graph.getInDegree(node) == 0:
            available.append(node)

    warning_str = ""
    while len(available) != 0:
        u = available.pop()
        graph.removeKey(u)

        print(f"{count}: {u}")
        count += 1
        unmentioned_warning = check_for_unlisted_prereqs(u, class_list)
        if len(unmentioned_warning) > 0:
            warning_str += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            warning_str += f"WARNING: Unlisted Prerequisites For {u}:\n"
            for lst in unmentioned_warning:
                warning_str += "- "+" OR ".join(lst)+'\n'
        
        for node in nodes:
            if graph.getInDegree(node) == 0 and not (node in available):
                available.append(node)

    if warning_str != "":
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Some classes may seem out of order due to these warnings:")
        print(warning_str.rstrip('\n'))



def run() -> None:
    """
    Runs program as intended.
    """
    
    # Prompt user for classes
    print("UCI Prerequisite Planner -- Developed by Julian Zulfikar, 2022")
    print("----------------------------------------------------------------------")
    print("Note: Classes must be formatted as DEPARTMENT 000")
    print("      i.e. COMPSCI 161, MATH 2B, I&C SCI 31")
    print("         - Input department as shown on Schedule of Classes\n")
    print("Questions/Bugs? Email: jzulfika@uci.edu")
    print("----------------------------------------------------------------------")

    print("Select Input Option:")
    print("'M' = Manually input courses one by one")
    print("'O' = Input classes as one-line")
    print("'F' = Read input line by line from file")
    valid_options = ['M','O','F']
    input_option = input("Option: ")
    while input_option not in valid_options:
        print("ERROR: Invalid option")
        input_option = input("Option: ")

    print("----------------------------------------------------------------------")

    # Manual input
    class_list = []
    if input_option == 'M':
        print("Input: Manually input classes, type 'DONE' when finished")
        print("----------------------------------------------------------------------")
        class_input = input("Class: ")
        while class_input != 'DONE':
            try:
                if valid_class(class_input):
                    if class_input in class_list:
                        print(f"ERROR: {class_input} already added.")
                    else:
                        class_list.append(class_input)
                        print(f"{class_input} added!")
                else:
                    print(f"ERROR: {class_input} either is invalid or has not been offered recently.")
            except:
                print(f"ERROR: {class_input} is not correctly formatted")

            class_input = input("Class: ")
    # One line input
    elif input_option == 'O':
        print("Input: One line input separated by commas")
        print("       i.e. 'I&C SCI 31,I&C SCI 32,I&C SCI 33'")
        print("Note: Invalid courses will be ignored!")
        print("----------------------------------------------------------------------")
        class_input = input("Classes: ")
        inputted_classes = class_input.split(',')
        print("Attempting to add classes...")
        for c in inputted_classes:
            try:
                if valid_class(c):
                    if c in class_list:
                        print(f"ERROR: {c} is already added. Has been skipped.")
                    else:
                        class_list.append(c)
                        print(f"{c} added!")
                else:
                    print(f"ERROR: {c} either is invalid or has not been offered recently.")
            except:
                print(f"ERROR: {c} is not correctly formatted")
    # File input
    else:
        print("Input: Name of file which holds one course on each line")
        print("Note: View sample_input.txt for an example!")
        print("----------------------------------------------------------------------")
        while True:
            filename = input("File: ")
            try:
                with open(filename, 'r') as f:
                    print("Attempting to add classes...")
                    for line in f:
                        c = line.rstrip('\n')
                        try:
                            if valid_class(c):
                                if c in class_list:
                                    print(f"ERROR: {c} is already added. Has been skipped.")
                                else:
                                    class_list.append(c)
                                    print(f"{c} added!")
                            else:
                                print(f"ERROR: {c} either is invalid or has not been offered recently.")
                        except:
                            print(f"ERROR: {c} is not correctly formatted")
                break # Done processing file
            except:
                print(f"ERROR: File {filename} is invalid. Make sure it is in the same folder as main.py!")

    print("----------------------------------------------------------------------")
    print("Initializing graph of classes...")
    print("----------------------------------------------------------------------")
    
    # Initialize graph
    class_graph = Graph(class_list)
    
    for c in class_list:
        class_list_no_c = list(class_list)
        class_list_no_c.remove(c)
        for d in class_list_no_c:
            print(f"Checking if {c} is a prerequisite to {d}...")
            if prereq(c,d):
                class_graph.addDirectedEdge(c,d)

    # Run topological sort algorithm
    print("----------------------------------------------------------------------")
    print("Sorting by prerequisites...")
    print("----------------------------------------------------------------------")
    _topological_sort(class_graph, class_list)

    print("----------------------------------------------------------------------")
    print("Questions/Bugs? Email: jzulfika@uci.edu")


if __name__ == "__main__":
    run()


