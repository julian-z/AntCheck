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
PAST_5_TERMS = [
    "2023%20Winter", "2022%20Fall",
    "2022%20Spring", "2022%20Winter",
    "2021%20Fall"
    ] # Most recent = priority
CACHE_PREREQ_STRS = dict()
CACHE_JSON = dict()
SPECIAL_CHAR_DEPTS = {
    "I&CSCI":"I%26C%20SCI", "CRM/LAW":"CRM%2FLAW",
    "ARTHIS":"ART%20HIS", "ACENG":"AC%20ENG",
    "ARTSTU":"ART%20STU", "BIOSCI":"BIO%20SCI",
    "CHC/LAT":"CHC%2FLAT", "COMLIT":"COM%20LIT",
    "DEVBIO":"DEV%20BIO", "EASIAN":"E%20ASIAN",
    "ECOEVO":"ECO%20EVO", "EUROST":"EURO%20ST",
    "FLM&MDA":"FLM%26MDA", "GEN&SEX":"GEN%26SEX",
    "INTLST":"INTL%20ST", "LITJRN":"LIT%20JRN",
    "MEDHUM":"MED%20HUM", "MGMTEP":"MGMT%20EP",
    "MGMTFE":"MGMT%20FE", "MOLBIO":"MOL%20BIO",
    "NETSYS":"NET%20SYS", "NURSCI":"NUR%20SCI",
    "PHYSCI":"PHY%20SCI", "POLSCI":"POL%20SCI",
    "PP&D":"PP%26D", "PSYBEH":"PSY%20BEH",
    "RELSTD":"REL%20STD", "SOCSCI":"SOC%20SCI",
    "UNISTU":"UNI%20STU", "WOMNST":"WOMN%20ST"
    }


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
    based on Schedule of Classes for PAST_5_TERMS.

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
    if B_department in SPECIAL_CHAR_DEPTS.keys():
        B_department = SPECIAL_CHAR_DEPTS[B_department]
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
    if X_department in SPECIAL_CHAR_DEPTS.keys():
        X_department = SPECIAL_CHAR_DEPTS[X_department]

    # Check if class has been offered in the past 5 terms
    for TERM in PAST_5_TERMS:
        query_parameters = [
            ("term", TERM),
            ("department", X_department),
            ("courseNumber", X_courseNumber)
        ]
        
        encoded = urllib.parse.urlencode(query_parameters, safe='%')
        url = f"{PETERPORTAL_BASE_URL}?{encoded}"
        
        try:
            # Using PeterPortal
            response_get = requests.get(url)
            response = response_get.json()

            # If class is invalid for TERM, json = {'schools': []}
            if (response != {'schools': []}):
                CACHE_JSON[x] = response
                return True
        except:
            return False
        finally:
            response_get.close()

    return False



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

