# classes_scrape.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Uses the PeterPortal API to obtain knowledge about classes.
# Note: The str of prerequisites is not meant to be pretty by any
#       means; simply used to figure out whether or not a class is
#       a prerequisite.
# Note: One weakness of this program is that Co-requisites are not
#       taken into account. As of 12/6/2022, they are being treated
#       as prerequisites.

import requests
import urllib.parse


PETERPORTAL_BASE_URL = "https://api.peterportal.org/rest/v0/schedule/soc"
CURRENT_TERM = "2022%20Fall"
CACHE_PREREQ_STRS = dict()
CACHE_JSON = dict()



def _try_peter_portal(url: str) -> (bool, dict):
    """
    Requests from PeterPortal API.

    Returns a 2-tuple:
    - 0 for fail, 1 for success
    - dict of JSON object
    """
    try:
        # Using PeterPortal
        response_get = requests.get(url)
        response = response_get.json()

        # If class is invalid, json = {'schools': []}
        if (response == {'schools': []}):
            return (False, dict())
        else:
            return (True, response)
    except:
        return (False, dict())
    finally:
        response_get.close()



def _get_prereq_str(url: str, courseTitle: str) -> str:
    """
    Scrapes the prerequisite link's source code to gather
    the prerequisite classes.
    """
    try:
        # Try to get the prereq site source code
        response_prereq_get = requests.get(url)
        response_prereq = response_prereq_get.text

        starting_index = response_prereq.find(courseTitle)
        end_index = response_prereq.find('<td class="course" nowrap>', starting_index)
        class_str = response_prereq[starting_index:end_index]
        class_str = class_str.replace(" ", '')
        for x in ["</td>", "</b>", "<b>", "</tr>", "<tr>"]:
            class_str = class_str.replace(x, '')
        class_str = class_str[class_str.find('"prereq">'):]
        
        return class_str
    except:
        return "ERROR"
    finally:
        response_prereq_get.close()



def prereq(a: str, b: str) -> bool:
    """
    Returns true/false if a is a prerequisite of b;
    based on Schedule of Classes for CURRENT_TERM.

    Parameters need to be in the form of: DEPARTMENT000
    - i.e. COMPSCI161
    """
    # Get data of class B
    b_og = b
    for i in range(len(b)):
        if b[i].isnumeric():
            b = b[:i]+','+b[i:]
            break
        
    B_department, B_courseNumber = tuple(b.split(','))
    if B_department == "I&CSCI":
        B_department = "I%26C%20SCI"
    elif B_department == "CRM/LAW":
        B_department = "CRM%2FLAW"
    b_data = CACHE_JSON[b] # CACHE_JSON guaranteed to have b if b is a valid course

    # Get prerequisites of class B
    B_courseTitle = b_data["schools"][0]["departments"][0]["courses"][0]["courseTitle"]
    prerequisite_url = b_data["schools"][0]["departments"][0]["courses"][0]["prerequisiteLink"]
    if len(prerequisite_url) == 0:
        return False # No prerequisites

    if b_og in CACHE_PREREQ_STRS.keys():
        prereq_str = CACHE_PREREQ_STRS[b_og]
    else:
        prereq_str = _get_prereq_str(prerequisite_url, B_courseTitle)
        CACHE_PREREQ_STRS[b_og] = prereq_str # Cache b's prereq_str for future use

    # Check if a is a prereq of b
    return prereq_str.find(a) != -1



def valid_class(x: str) -> bool:
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
            CACHE_JSON[x] = response
            return True
    except:
        return False
    finally:
        response_get.close()



## ------------------------------------------------------------------
##    This section was used to experiment with scraping the pre-
##    requisites for each class; PeterPortal API does not support
##    this in their JSON data. Thus, the information was gathered
##    from the prerequisite course link's source code.
##
##    Feel free to uncomment and run from __main__ to see how it
##    works (gathering prereqs).
## ------------------------------------------------------------------
##
##if __name__ == "__main__":
##
##    cs_class_nums = ['112','115','117','121','122A','122B',
##                     '132','134','141','143A','151','161',
##                     '163','169','171','175','178',
##                     '183','184A','274E']
##    
##    for x in cs_class_nums:
##        print("---------------------------------------------")
##        
##        # Using PeterPortal
##        url = "https://api.peterportal.org/rest/v0/schedule/soc?term=2022%20Fall&department=COMPSCI&courseNumber="
##        response_attempt = requests.get(url+x)
##        # print(response.status_code)
##        # If class is invalid, json = {'schools': []}
##        response = response_attempt.json()
##        response_attempt.close()
##
##        # courseTitle
##        courseTitle = response["schools"][0]["departments"][0]["courses"][0]["courseTitle"] 
##        print( courseTitle )
##
##        # Prereq link
##        prerequisiteLink = response["schools"][0]["departments"][0]["courses"][0]["prerequisiteLink"]
##        print( prerequisiteLink )
##
##        print("---------------------------------------------")
##
##        # Getting the prereq site source code
##        response_prereq = requests.get(prerequisiteLink)
##        response_prereq = response_prereq.text
##        
##        starting_index = response_prereq.find(courseTitle)
##        end_index = response_prereq.find('<td class="course" nowrap>', starting_index)
##        class_str = response_prereq[starting_index:end_index]
##        class_str = class_str.replace(" ", '')
##        for x in ["</td>", "</b>", "<b>", "</tr>", "<tr>"]:
##            class_str = class_str.replace(x, '')
##        class_str = class_str[class_str.find('"prereq">'):]
##        print(class_str)
##
##        # Decided not to split into a list due to formatting issues
##        # prereq_list = class_str.split("AND")
##        # for prereq in prereq_list:
##        #    print(prereq[:prereq.find("\r")])
##
##    # Testing prereq()
##    print( prereq("I&CSCI31", "I&CSCI32") )
##    print( prereq("MATH2B", "STATS67") )
##    print( prereq("STATS7", "COMPSCI121") )


