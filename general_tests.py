# general_tests.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Unit tests used for Test Driven Development.

from graph import *
from classes_scrape import *
import unittest
import random


class GraphTest(unittest.TestCase):
    def test_simpleInit(self):
        # Initialize a random graph with no edges
        random_numKeys = random.randint(0,100)
        random_list_of_keys = list(range(0, random_numKeys))
        test_graph = Graph(random_list_of_keys)

        self.assertEqual( test_graph.getNumKeys(), random_numKeys )
        for i in range(0, random_numKeys):
            self.assertEqual( test_graph.getEdges(i), set() )
            self.assertEqual( test_graph.getInDegree(i), 0 )
            self.assertEqual( test_graph.getOutDegree(i), 0 )

    def test_simpleEdges(self):
        # Testing addDirectedEdge
        keys = ['a','b','c','d']
        test_graph = Graph(keys)
        test_graph.addDirectedEdge('a','b')
        test_graph.addDirectedEdge('a','c')
        test_graph.addDirectedEdge('a','d')
        a_edges = {'b','c','d'}

        # Testing getEdges
        self.assertEqual( test_graph.getEdges('a'), a_edges )
        self.assertEqual( test_graph.getEdges('b'), set() )
        self.assertEqual( test_graph.getEdges('c'), set() )
        self.assertEqual( test_graph.getEdges('d'), set() )

        # Testing inDegree
        self.assertEqual( test_graph.getInDegree('a'), 0 )
        self.assertEqual( test_graph.getInDegree('b'), 1 )
        self.assertEqual( test_graph.getInDegree('c'), 1 )
        self.assertEqual( test_graph.getInDegree('d'), 1 )

        # Testing outDegree
        self.assertEqual( test_graph.getOutDegree('a'), 3 )
        self.assertEqual( test_graph.getOutDegree('b'), 0 )
        self.assertEqual( test_graph.getOutDegree('c'), 0 )
        self.assertEqual( test_graph.getOutDegree('d'), 0 )

        # Testing removeDirectedEdge
        test_graph.removeDirectedEdge('a','b')
        test_graph.removeDirectedEdge('a','c')
        a_edges.remove('b')
        a_edges.remove('c')
        self.assertEqual( test_graph.getEdges('a'), a_edges )
        self.assertEqual( test_graph.getEdges('b'), set() )
        self.assertEqual( test_graph.getEdges('c'), set() )
        self.assertEqual( test_graph.getEdges('d'), set() )
        self.assertEqual( test_graph.getInDegree('a'), 0 )
        self.assertEqual( test_graph.getInDegree('b'), 0 )
        self.assertEqual( test_graph.getInDegree('c'), 0 )
        self.assertEqual( test_graph.getInDegree('d'), 1 )
        self.assertEqual( test_graph.getOutDegree('a'), 1 )
        self.assertEqual( test_graph.getOutDegree('b'), 0 )
        self.assertEqual( test_graph.getOutDegree('c'), 0 )
        self.assertEqual( test_graph.getOutDegree('d'), 0 )


class PrereqTest(unittest.TestCase):
    def test_ICS_trilogy(self):
        # 31 -> 32 -> 33
        self.assertTrue( prereq("I&CSCI31", "I&CSCI32") )
        self.assertTrue( prereq("I&CSCI32", "I&CSCI33") )
        self.assertFalse( prereq("I&CSCI32", "I&CSCI31") )
        self.assertFalse( prereq("I&CSCI33", "I&CSCI32") )

    def test_CS_161(self):
        # 161 Prerequisites: 46, 6B, 6D, 2B
        self.assertTrue( prereq("I&CSCI46", "COMPSCI161") )
        self.assertTrue( prereq("I&CSCI6B", "COMPSCI161") )
        self.assertTrue( prereq("I&CSCI6D", "COMPSCI161") )
        self.assertTrue( prereq("MATH2B", "COMPSCI161") )


if __name__ == '__main__':
    unittest.main()

