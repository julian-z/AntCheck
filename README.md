# ClassPlanner
Created by Julian Zulfikar, project started on 12-6-2022.

# Description
This Class Planner takes a given set of UCI classes that you intend to take; could be in the current schoolyear or throughout your entire career.

With this set, a directed graph is initialized with edges representing courses that must be taken beforehand.

A topological sort is then performed on such graph; returning a sorted order of classes that can be taken where prerequisites are not violated.

# How To Use
Directions and sample inputs are provided. Actively seeking for ways to optimize user experience.

# Files
Each file is well-documented with summaries at the top.

classes_scrape.py: Utilizes UCI's PeterPortal API & scrapes the source code of UCI's Schedule of Classes website to collect prerequisites
graph.py: Hash-map adjacency list of a graph implementation
general_tests.py: Unit tests for test-driven development
main.py: run() function, creates a topological sort of given classes

# Shortcomings
Due to the limitations of the API not having a list of prerequisite courses readily available, the prerequisites are checked via web scraping.

The source code of UCI's Schedule of Classes may not have some courses listed, which may lead to the program thinking it is not in the database.

# Current Stage of Development
Development phase is extremely early on, as of December 2022. Looking to make as many optimizations as possible to cut down runtime.

# Conclusion
Open to suggestions! Email me at jzulfika@uci.edu