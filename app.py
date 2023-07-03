# app.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Uses the Flask framework, HTML, and CSS to create a website
# implementation of ZotPlanner.

from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

from query import prereq, valid_class, check_for_unlisted_prereqs
from graph import Graph

app = Flask(__name__)
COURSE_LIST = []


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Renders the homepage.
    """
    if request.method == 'POST':
        dept = request.form['drop']
        course_num = request.form['search']

        if (len(course_num) == 0) or (not course_num[0].isnumeric()):
            return render_template('index.html', courses=COURSE_LIST, errormsg="Error adding class.")

        if (dept+course_num not in COURSE_LIST) and valid_class(dept+' '+course_num):
            COURSE_LIST.append(dept+' '+course_num)
        else:
            return render_template('index.html', courses=COURSE_LIST, errormsg="Error adding class.")

        return render_template('index.html', courses=COURSE_LIST, errormsg="")
    else:
        return render_template('index.html', courses=COURSE_LIST, errormsg="")


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
    return render_template('index.html', courses=COURSE_LIST, errormsg="")


if __name__ == '__main__':
    app.run(debug=True)

