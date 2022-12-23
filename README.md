![](https://github.com/julian-z/ZotPlanner/blob/main/static/images/zotplannerlogo.png)
Created by Julian Zulfikar, December 2022.

# Purpose
Prerequisites can be confusing, and the goal of this project is to help students figure out the correct order in which they should enroll in their classes!

ZotPlanner takes a given set of UCI classes that you intend to take; could be in the current schoolyear or throughout your entire career.

The user is then given an ordering of classes that they are able to take such that no prerequisites requirements are violated.

The program also warns the user if they did not include a required prerequisite in their input. For example, if a student is looking to take CS 161 and they input {ICS 46, ICS 6D, CS 161}, the program would warn them of 161's ICS 6B & Math 2B requirement. You'll never miss a prerequisite again!

![](https://github.com/julian-z/ZotPlanner/blob/main/images/zotplannerdemo.gif)

# How It Works
The user inputs a set of classes they are looking to take. From there, a directed graph is initialized with edges representing courses that must be taken beforehand.

A topological sort is then performed on such graph; returning a sorted order of classes that can be taken where prerequisites are not violated.

The program uses UCI's PeterPortal API in order to look up the class in the database. However, the current implementation of the API does not provide a list of classes that are considered prerequisites. In order to combat this, the Schedule of Classes website's source code is scraped in order to check whether or not a given class is a prerequisite to another.

![](https://github.com/julian-z/ZotPlanner/blob/main/images/topologicalsort.gif)

# Optimizations
You may be wondering: if the graph of classes has to be formed on the fly, wouldn't the program be very slow & take a lot of API requests?

To fight this, after every valid URL request from the API & the Schedule of Classes, we "memoize" the data, which keeps it in a cache for later use. This shortens the runtime drastically, as without it, we would have to request to check the prerequisites for every pair of classes, which would grow to be extremely slow the more classes are inputted.

# How To Use
Directions and sample input files are provided. Actively seeking for ways to optimize user experience.

As of 12-8-2022, in the Python Shell version, the user is able to manually input classes one-by-one, input it via CSV one-liner, or a file input (demonstrated by sample_input.txt).

As of 12-10-2022, a localhost website is available.

12-12-22 Screenshots:
![](https://github.com/julian-z/ZotPlanner/blob/main/images/index.png)
![](https://github.com/julian-z/ZotPlanner/blob/main/images/generate.png)

# Files
Each file is well-documented with summaries at the top.

classes_scrape.py: Utilizes UCI's PeterPortal API & scrapes the source code of UCI's Schedule of Classes website to collect prerequisites

graph.py: Hash-map adjacency list of a graph implementation

general_tests.py: Unit tests for test-driven development

main.py: run() function, creates a topological sort of given classes

app.py: Utilizes Flask framework for website implementation

# Shortcomings
Since UCI's course database isn't readily available, the program has to check the past 5 quarters to decide if it is a valid class. Though, it may be very unlikely that a class has not been offered since then & is still relevant.

# Future Endeavors
Development phase is extremely early on, as of December 2022. Looking to make as many optimizations as possible.

Currently, the website implementation can only be run on localhost, as I am currently looking to host it somewhere that will allow the API to be used.

# Conclusion
Open to suggestions! Email me at jzulfika@uci.edu
