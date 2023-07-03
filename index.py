# index.py - Julian Zulfikar, 2023
# ------------------------------------------------------------------
# Scrapes UCI's links of classes, parses the html, and builds an 
# index object (JSON).
#
#   Index takes the form of:
#   {
#       class: [department, title, description, prerequisites], ...
#   }

import requests
from unidecode import unidecode
from lxml import html
import ujson

COURSES_URL = "https://catalogue.uci.edu/allcourses/"


class DepartmentException(Exception):
    pass


class Course:
    def __init__(self, course, title, dept, description):
        self.course = course
        self.title = title
        self.dept = dept
        self.description = description
        self.prereq_str = ""


class Index:
    def __init__(self):
        self._index = {}


    def format_dept(self, course: str) -> str:
        """
        Extracts the department from a course.
        """
        end_index = len(course)-1

        while end_index >= 0:
            if ord(course[end_index]) == 160:
                return course[:end_index]
            else:
                end_index -= 1
        
        raise DepartmentException()


    def format_course_info(self, course_info: str) -> Course:
        """
        Returns a Course object:
            (course, title, dept, description)
        """
        course = course_info[:course_info.index('.', 0)]
        cur = course_info.index('.', 0)

        title = course_info[cur+3:course_info.index('.', cur+1)]

        dept = self.format_dept(course)

        first_newline = course_info.index('\n')
        description = course_info[first_newline+1:course_info.index('\n', first_newline+1)]

        return Course(unidecode(course), unidecode(title), unidecode(dept), unidecode(description))


    def create_index(self) -> None:
        """
        Obtains course links of every department.
            Crawls each link and parses the source code to obtain:
                - Course titles
                - Course IDs
                - Course descriptions
                - Course prerequisites
        
        Writes resulting index into JSON txt file (index.txt).
            Index takes the form of:
            {
                class: [department, title, description, prerequisites], ...
            }
        """
        
        print("Obtaining course links of departments...")
        # Get the course site source code
        # - Trims source code to section with department links
        page_content_get = requests.get(COURSES_URL).text
        start_index = page_content_get.index('<h2 class="letternav-head" id=\'A\'><a name=\'A\'>A</a></h2>')
        end_index = page_content_get.index('</div><!--end #textcontainer -->', start_index)
        page_content = html.fromstring(page_content_get[start_index:end_index])
        page_content.make_links_absolute(COURSES_URL)

        # Retrieve all department specific links
        dept_links = []
        for info in page_content.iterlinks():
            if info[1] == "href":
                dept_links.append(info[2])

        # Try to open each link and write index to file
        errors = []
        for link in dept_links:   
            print("Scraping link:", link)         
            try:
                # Extracting html content
                course_content_get = requests.get(link).text
                start_index = course_content_get.index('<div id="courseinventorycontainer" class="page_content tab_content">')
                end_index = course_content_get.index('<footer>', start_index)
                course_content_get = course_content_get[start_index:end_index]
                courses = [html.fromstring(section).xpath("string()") for section in course_content_get.split('<div class="courseblock">')][1:]
            except:
                print("ERROR PARSING PAGE:", link)
                errors.append(link)
            else:
                for c in courses:
                    course_obj = self.format_course_info(c)
                    prereq_index = c.find('Prerequisite')
                    if prereq_index != -1:
                        prereq_str = c[prereq_index+14:c.find('\n', prereq_index+14)]
                        course_obj.prereq_str = unidecode(prereq_str)
                    
                    self._index[course_obj.course] = [course_obj.dept, course_obj.title, course_obj.description, course_obj.prereq_str]
                    # print([course_obj.course, course_obj.dept, course_obj.title, course_obj.description, course_obj.prereq_str])
                    print("Written", course_obj.course)

        print("Writing index into file...")
        # Dumps index into json
        with open("index.txt", 'w') as index:
            ujson.dump(self._index, index)
        
        print("Index completed!")
        print("Error count:", len(errors))
        for link in errors:
            print(link)
        
    
    def get_index(self) -> dict:
        if len(self._index) != 0:
            return self._index
        else:
            with open("index.txt", 'r') as f:
                return ujson.load(f)


if __name__ == "__main__":
    index = Index()
    index.create_index()

