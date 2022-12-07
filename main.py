# main.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Utilizes an adjacency list graph implementation as well as an API
# & source code scraper to create a topological sort of classes.
# A.K.A. an ordering of classes such that if taken in order,
# prerequisites will not be violated.

from classes_scrape import prereq
from graph import Graph
import requests
import urllib.parse


PETERPORTAL_BASE_URL = "https://api.peterportal.org/rest/v0/schedule/soc"
CURRENT_TERM = "2022%20Fall"



def _valid_class(x: str) -> bool:
    """
    Requests from PeterPortal API in order to check for validity of class.
    """
    # Get URL of class X
    for i in range(len(x)):
        if x[i].isnumeric():
            x = x[:i]+','+x[i:]
            break
    X_department, X_courseNumber = tuple(x.split(','))
    if X_department == "I&CSCI":
        X_department = "I%26C%20SCI"
    elif X_department == "CRM/LAW":
        X_department = "CRM%2FLAW"
        
    query_parameters = [
        ("term", CURRENT_TERM),
        ("department", X_department),
        ("courseNumber", X_courseNumber)
    ]
    
    encoded = urllib.parse.urlencode(query_parameters, safe='%')
    url = f"{PETERPORTAL_BASE_URL}?{encoded}"
    
    try:
        # Using PeterPortal
        response_get = requests.get(url)
        response = response_get.json()

        # If class is invalid, json = {'schools': []}
        if (response == {'schools': []}):
            return False
        else:
            return True
    except:
        return False
    finally:
        response_get.close()



def _topological_sort(graph: 'Graph', nodes: list) -> None:
    """
    Outputs a topological sort by repeatedly removing nodes
    with 0 in-degree.

    Citation: Professor Michael Shindler, ICS-46
    """
    count = 1

    available = []
    for node in nodes:
        if graph.getInDegree(node) == 0:
            available.append(node)

    while len(available) != 0:
        u = available.pop()
        graph.removeKey(u)

        print(f"{count}: {u}")
        count += 1
        
        for node in nodes:
            if graph.getInDegree(node) == 0 and not (node in available):
                available.append(node)



def run() -> None:
    """
    Runs program as intended.
    """
    # Prompt user for classes
    print("UCI Prerequisite Planner -- Developed by Julian Zulfikar, 2022")
    print("--------------------------------------------------------------")
    print("Input: Classes you intend to take")
    print("       'DONE' to finish inputting classes\n")
    print("Note: Classes must be formatted as DEPARTMENT000")
    print("      i.e. COMPSCI161, MATH2B")
    print("      - If a department has spaces (I&C SCI), do not include")
    print("      - Input department as shown on Schedule of Classes\n")
    print("Questions/Bugs? Email: jzulfika@uci.edu")
    print("--------------------------------------------------------------")

    class_list = []
    class_input = input("Class: ")
    while class_input != 'DONE':
        if class_input.find(" ") != -1:
            print(f"ERROR: Remove spaces.")
        elif _valid_class(class_input):
            if class_input in class_list:
                print(f"ERROR: Class {class_input} already added.")
            else:
                class_list.append(class_input)
                print(f"{class_input} added!")
        else:
            print(f"ERROR: Class {class_input} either is not valid or is not in the database.")

        class_input = input("Class: ")

    print("--------------------------------------------------------------")
    print("Initializing graph of classes...")
    print("--------------------------------------------------------------")
    
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
    print("--------------------------------------------------------------")
    print("Sorting by prerequisites...")
    print("--------------------------------------------------------------")
    top_sort = _topological_sort(class_graph, class_list)

    print("--------------------------------------------------------------")
    print("NOTE: As of 12-6-22, corequisites are treated as prerequisites!")
    print("Questions/Bugs? Email: jzulfika@uci.edu")



if __name__ == "__main__":
    run()


