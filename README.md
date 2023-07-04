![](https://github.com/julian-z/ZotPlanner/blob/main/static/images/zotplannerlogo.png)
Created by Julian Zulfikar, December 2022.
https://zotplanner.pythonanywhere.com/

# Purpose 📋
Courses and prerequisites can be very overwhelming for students, which is why the goal of this project is to provide an improved user experience when it comes to browsing the catalogue and selecting the correct order in which they should enroll in their classes!

ZotPlanner takes a given set of UCI classes that you intend to take -- could be in the current schoolyear or throughout your entire career.

The user is then given an ordering of classes that they are able to take such that no prerequisites requirements are violated.

The program also warns the user if they did not include a required prerequisite in their input. For example, if a student is looking to take CS 161 and they input {ICS 46, ICS 6D, CS 161}, the program would warn them of 161's ICS 6B & Math 2B requirement. You'll never miss a prerequisite again!

The search engine also provides a swift and easy way for students to browse through UCI's catalogue of over 5900 classes. The results are ranked in order of relevancy by TF-IDF score.

![](https://github.com/julian-z/ZotPlanner/blob/main/images/zotplanner.gif)

# How It Works 🧠
The user inputs a set of classes they are looking to take. From there, a directed graph is initialized with edges representing courses that must be taken beforehand.

A topological sort is then performed on such graph, returning a sorted order of classes that can be taken where prerequisites are not violated.

To easily retrieve information on how classes are related to each other, the program stores an index keeping track of course titles, descriptions, prerequisites, etc. The search engine relies on an inverted index, which uses words/tokens as search keys instead of courses.

![](https://github.com/julian-z/ZotPlanner/blob/main/images/topologicalsort.gif)

# Optimizations 🚀
You may be wondering: if the graph of classes has to be formed on the fly, wouldn't the program be very slow & take a lot of API requests?

Previously, (prior to July 2023) the program used the PeterPortal API to find prerequisite links, however, this was a major bottleneck due to the reason above. The optimization made to combat this issue was to memoize/cache every call, thus building an index as the program ran.

As of now, a web-crawler has been built which goes through every course page of each department. The data of each course is then collected, and thus, we quickly retrieve any information we need through an index.

# How To Use 💻
Directions and sample input files are provided. Actively seeking for ways to optimize user experience.

As of 12-8-2022, in the Python Shell version, the user is able to manually input classes one-by-one, input it via CSV one-liner, or a file input (demonstrated by sample_input.txt).

As of 12-10-2022, a localhost website is available.

As of 7-3-2023, a search engine implementation has been applied.

As of 7-4-2023, ZotPlanner has been deployed for demonstration: https://zotplanner.pythonanywhere.com/

7-4-2023 Screenshots:
![](https://github.com/julian-z/ZotPlanner/blob/main/images/1.png)
![](https://github.com/julian-z/ZotPlanner/blob/main/images/2.png)
![](https://github.com/julian-z/ZotPlanner/blob/main/images/3.png)
![](https://github.com/julian-z/ZotPlanner/blob/main/images/4.png)

# Files 📁
Each file is well-documented with summaries at the top.

index.py: Crawls through UCI's courses and builds an index for easy look-up

query.py: Retrieves information from the index of courses

graph.py: Hash-map adjacency list of a graph implementation

main.py: run() function, creates a topological sort of given classes

search.py: query_catalogue() function, serves as algorithm for search engine

app.py: Utilizes Flask framework for website implementation

# Conclusion 👋
Open to suggestions! Email me at jzulfika@uci.edu
