
The [Graph_Pairwise_Similarity_Calculation.ipynb](./Graph_Pairwise_Similarity_Calculation.ipynb) notebook explains how to calculate the graph edit distance between two coarse-grained graph representations of macromolecules using the A* method, as well as how to compute graph similarity using graph kernel methods. We refer to and modify the source code from GLAMOUR. The detailed modifications are described below.

1. The setting of the graph is changed from directional to non-directional in [utils/load_networkx.py](./utils/load_networkx.py).
   ``````
   graph = nx.Graph()
   ``````
2. The graph edit distance removes the edge substitution cost in [utils/macro_unsupervised.py](./utils/macro_unsupervised.py). In this MacroSimGNN work, the edges are the connections between nodes and do not have chemical features.
   
