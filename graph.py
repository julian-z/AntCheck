# graph.py - Julian Zulfikar, 2022
# ------------------------------------------------------------------
# Directed graph implementation using adjacency lists in a hash-map.
# Keeps track of in-degree and out-degree to figure out the order of
# prerequisites (topological sort).

from collections import defaultdict


class UnknownVertexError(Exception):
    pass


class UnknownEdgeError(Exception):
    pass


class Graph:
    def __init__(self, keys=[]):
        """
        Initialize a hash-map adjacency list graph
        - Can be given a list of keys
        """
        self._map = defaultdict(set)
        self._inDegree = defaultdict(int)
        self._outDegree = defaultdict(int)

        self._keys = keys
        
        for k in keys:
            self._map[k]
            self._inDegree[k]
            self._outDegree[k]
    

    def addDirectedEdge(self, u, v) -> None:
        """
        Add a directed edge from u->v

        Exceptions:
        UnknownVertexError if u or v is not found in the graph
        """
        if not (u in self._keys):
            raise UnknownVertexError
        if not (v in self._keys):
            raise UnknownVertexError

        self._map[u].add(v)
        self._outDegree[u] += 1
        self._inDegree[v] += 1
    

    def removeDirectedEdge(self, u, v) -> None:
        """
        Removes a directed edge from u->v

        Exceptions:
        UnknownVertexError if u or v is not found in the graph
        UnknownEdgeError if u->v is not found in the graph
        """
        if not (u in self._keys):
            raise UnknownVertexError
        if not (v in self._keys):
            raise UnknownVertexError
        if not (v in self._map[u]):
            raise UnknownEdgeError
        
        self._map[u].remove(v)
        self._outDegree[u] -= 1
        self._inDegree[v] -= 1
    

    def addKey(self, k) -> None:
        """
        Adds k as a key with zero edges (noexcept)
        - If k is already a key, function does not do anything
        """
        if (k in self._keys):
            return
        
        self._map[k]
        self._keys.append(k)
    

    def getEdges(self, k) -> set:
        """
        Returns k's set of edges

        Exceptions:
        UnknownVertexError if k is not found in the graph
        """
        if not (k in self._keys):
            raise UnknownVertexError
        
        return self._map[k]
    

    def getInDegree(self, k) -> int:
        """
        Returns k's in degree

        Exceptions:
        UnknownVertexError if k is not found in the graph
        """
        if not (k in self._keys):
            raise UnknownVertexError
        
        return self._inDegree[k]


    def getOutDegree(self, k) -> int:
        """
        Returns k's out degree

        Exceptions:
        UnknownVertexError if k is not found in the graph
        """
        if not (k in self._keys):
            raise UnknownVertexError
        
        return self._outDegree[k]


    def getNumKeys(self) -> int:
        """
        Return the current number of keys (noexcept)
        """
        return len(self._keys)

