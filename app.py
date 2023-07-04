# app.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Uses the Flask framework, HTML, and CSS to create a website
# implementation of ZotPlanner.

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from query import prereq, valid_class, check_for_unlisted_prereqs
from graph import Graph
from search import query_catalogue, DATA_INDEX

app = Flask(__name__)
COURSE_LIST = []


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Renders the homepage.
    """
    if request.method == 'POST':
        if 'course_num' in request.form:
            dept = request.form['drop']
            course_num = request.form['course_num']

            if (len(course_num) == 0) or (not course_num[0].isnumeric()):
                return render_template('index.html', search_results=[], courses=COURSE_LIST, errormsg="Error adding class.")

            if (dept+course_num not in COURSE_LIST) and valid_class(dept+' '+course_num):
                COURSE_LIST.append(dept+' '+course_num)
            else:
                return render_template('index.html', search_results=[], courses=COURSE_LIST, errormsg="Error adding class.")
        else:
            query = request.form['search_courses']

            print("SEARCHING CATALOGUE:", query)
            
            search_results = []
            for i, course in enumerate(query_catalogue(query)):
                if i >= 20:
                    break
                search_results.append((course, DATA_INDEX[course][1], DATA_INDEX[course][2], DATA_INDEX[course][3]))

            return render_template('index.html', search_results=search_results, courses=COURSE_LIST, errormsg="")

        return render_template('index.html', search_results=[], courses=COURSE_LIST, errormsg="")
    else:
        return render_template('index.html', search_results=[], courses=COURSE_LIST, errormsg="")


def _topological_sort(graph: 'Graph', nodes: list) -> None:
    """
    Outputs a topological sort by repeatedly removing nodes
    with 0 in-degree.

    Citation: Professor Michael Shindler, ICS-46

    - Modified from main.py to return (list, list)
    """
    result = []
    count = 1
    class_list = graph.getKeys()

    available = []
    for node in nodes:
        if graph.getInDegree(node) == 0:
            available.append(node)

    warning_lst = []
    while len(available) != 0:
        u = available.pop()
        graph.removeKey(u)

        result.append(f"{count}: {u}")
        count += 1
        unmentioned_warning = check_for_unlisted_prereqs(u, class_list)
        if len(unmentioned_warning) > 0:
            lst = []
            lst.append(f"WARNING: Unlisted Prerequisites For {u}:")
            for l in unmentioned_warning:
                lst.append("- "+" OR ".join(l))
            warning_lst.append(lst)
        
        for node in nodes:
            if graph.getInDegree(node) == 0 and not (node in available):
                available.append(node)
    
    return (result, warning_lst)


@app.route('/generate')
def generate():
    """
    Generates a directed graph and finds a topological sort of classes.
    """
    try:
        # Initialize graph
        global COURSE_LIST
        class_graph = Graph(COURSE_LIST)
        
        for c in COURSE_LIST:
            class_list_no_c = list(COURSE_LIST)
            class_list_no_c.remove(c)
            for d in class_list_no_c:
                if prereq(c,d):
                    class_graph.addDirectedEdge(c,d)
        
        # Run topological sort algorithm
        result_lst, warning_lst = _topological_sort(class_graph, COURSE_LIST)

        return render_template('generate.html', order=result_lst, warning=warning_lst)
    except:
        return render_template('generate.html', order=["FATAL"], warning="Something very unexpected has occurred. Apologize for the inconvenience.")


@app.route('/clear')
def clearCourses():
    """
    Clears the current list of added courses.
    """
    global COURSE_LIST
    COURSE_LIST = []
    return render_template('index.html', search_results=[], courses=COURSE_LIST, errormsg="")


if __name__ == '__main__':
    app.run(debug=True)

