# query.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Retrieves information from the index.

from index import Index


INDEX = Index().get_index()


def prereq(a: str, b: str) -> bool:
    """
    Checks if course a is a prerequisite to course b.
    """
    return INDEX[b][3].find(a) != -1


def valid_class(x: str) -> bool:
    """
    Checks if course x is a valid course.
    """
    return x in INDEX


def check_for_unlisted_prereqs(course: str, class_list: list):
    """
    Checks for any prerequisites not listed.
        i.e. Input is ICS 33 and ICS 6B -- the program will
             warn them that ICS 32 is a prerequisite to 33,
             since they did not input it themselves.
    """
    if not INDEX[course][3]:
        return []
    
    prereq_str = INDEX[course][3]
    prereq_list_before_OR = prereq_str.split(" and ")
    prereq_list = [c.split(" or ") for c in prereq_list_before_OR]

    for course in class_list:
        for i in range(len(prereq_list)):
            if any( True if c.find(course) != -1 else False for c in prereq_list[i] ):
                prereq_list[i] = []
    
    prereq_list = [x for x in prereq_list if x != [] and x != ['']]
    return prereq_list

