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

import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

from math import log10

# Run these lines once to download packages for lemmatization
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

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
        self._inverted_index = {}

        self._stopwords = set(stopwords.words('english'))
        self._lemmatizer = WordNetLemmatizer()


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
        Obtains course links of every department and creates index.
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

        # Dumps index into json
        print("Writing index into file...")
        with open("index.txt", 'w') as index:
            ujson.dump(self._index, index)
        
        print("Index completed!")
        print("Error count:", len(errors))
        for link in errors:
            print(link)
        
    
    def create_inverted_index(self):
        """
        Obtains course links of every department and creates inverted index.
            Crawls each link and parses the source code to obtain:
                - Course titles
                - Course IDs
                - Course descriptions
                - Course prerequisites

        Writes resulting index into JSON txt file (inverted_index.txt).
            Index takes the form of:
            {
                token: [
                    [course, frequency, tf-idf]
                ], ...
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
        num_courses = 0
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
                    num_courses += 1

                    # Add tokens from title and description into inverted index
                    # - Note: Title tokens are weighed 3x higher
                    title_tokens = set(self._lemmatize_with_pos(token) for token in wordpunct_tokenize(course_obj.title))-self._stopwords
                    tokens = [self._lemmatize_with_pos(token) for token in wordpunct_tokenize(course_obj.title)]
                    tokens += [self._lemmatize_with_pos(token) for token in wordpunct_tokenize(course_obj.description)]
                    tokens = set(tokens)-self._stopwords
                    for token in tokens:
                        add = 1 if token not in title_tokens else 3

                        if token not in self._inverted_index:
                            self._inverted_index[token] = [[course_obj.course, add]]
                        else:
                            for i in range(len(self._inverted_index[token])):
                                if self._inverted_index[token][i][0] == course_obj.course:
                                    break
                            
                            if self._inverted_index[token][i][0] == course_obj.course:
                                self._inverted_index[token][i][1] += add
                            else:
                                self._inverted_index[token].append([course_obj.course, add])
                    
                    print("Written", course_obj.course)
        
        # Writing TF-IDF scores
        print("Writing TF-IDF scores...")
        for token in self._inverted_index:
            print("Writing token:", token)
            for page in self._inverted_index[token]:
                tf_idf = 0 if 1+log10(page[1]) <= 0 else \
                        (1+log10(page[1]))*(log10(num_courses/len(self._inverted_index[token])))
                page.append(tf_idf)

        # Dumps inverted index into json
        print("Writing inverted index into file...")
        with open("inverted_index.txt", 'w') as inverted_index:
            ujson.dump(self._inverted_index, inverted_index)
        
        print("Inverted Index completed!")
        print("Error count:", len(errors))
        for link in errors:
            print(link)


    def create_index_by_dept(self) -> None:
        """
        Obtains course links of every department and creates separate indexes.
            Crawls each link and parses the source code to obtain:
                - Course titles
                - Course IDs
                - Course descriptions
                - Course prerequisites
        
        Writes resulting index into JSON txt file(s) (dept_index.txt).
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
        depts = []
        dept_indexes = []
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
                if len(courses):
                    dept = self.format_course_info(courses[0]).dept
                    depts.append(dept)
                    dept_index = {}

                    for c in courses:
                        course_obj = self.format_course_info(c)
                        prereq_index = c.find('Prerequisite')
                        if prereq_index != -1:
                            prereq_str = c[prereq_index+14:c.find('\n', prereq_index+14)]
                            course_obj.prereq_str = unidecode(prereq_str)
                        
                        dept_index[course_obj.course] = [course_obj.dept, course_obj.title, course_obj.description, course_obj.prereq_str]
                        print("Written", course_obj.course)
                    
                    dept_indexes.append(dept_index)

        # Dumps index into json
        print("Writing indexes into files...")
        for i, dept in enumerate(depts):
            result = ""
            for x in dept:
                if x.isalnum():
                    result += x
            with open(f"dept/{result}_index.txt", 'w') as index:
                ujson.dump(dept_indexes[i], index)
        
        print("Index completed!")
        print("Error count:", len(errors))
        for link in errors:
            print(link)

        
    def get_index(self) -> dict:
        """
        If the index has already been created in the same run, return it.
            Otherwise, open the file.
        """
        if len(self._index) != 0:
            return self._index
        else:
            with open("index.txt", 'r') as f:
                self._index = ujson.load(f)
            return self._index


    def get_inverted_index(self) -> dict:
        """
        Refer to get_index.
        """
        if len(self._inverted_index) != 0:
            return self._inverted_index
        else:
            with open("inverted_index.txt", 'r') as f:
                self._inverted_index = ujson.load(f)
            return self._inverted_index


    def _lemmatize_with_pos(self, token: str) -> str:
        """
        Perform lemmatization with a parts-of-speech tagger.
        """
        tag = nltk.pos_tag([token])[0][1][0]

        if tag == 'N': tag = wordnet.NOUN
        elif tag == 'V': tag = wordnet.VERB
        elif tag == 'R': tag = wordnet.ADV
        elif tag == 'J': tag = wordnet.ADJ
        else: return token.lower()

        return self._lemmatizer.lemmatize(token, pos=tag).lower()


if __name__ == "__main__":
    index = Index()
    index.create_index()
    index.create_inverted_index()

