# MacroSimGNN

This repository supports the following manuscript. 

Jiale Shi, Dylan J. Walsh, Runzhong Wang, Nathan J. Rebello, Bradley D. Olsen, Debra J. Audus. "MacroSimGNN: Efficient and Accurate Calculation of Macromolecule Pairwise Similarity via Graph Neural Network," ChemRxiv, 2024.


Efficient and accurate calculation of macromolecule pairwise similarity is essential for developing database search engines and is useful for machine learning based predictive tools. Existing methods for calculating macromolecular similarity suffer from significant drawbacks. Graph edit distance is accurate but computationally expensive, and graph kernel methods are computationally efficient but inaccurate. This study introduces a graph neural network model, MacroSimGNN, which significantly improves computational efficiency while maintaining high accuracy on macromolecule pairwise similarity. Furthermore, this approach enables feature embeddings based on macromolecular similarities to a set of landmark molecules, enhancing both unsupervised and supervised learning tasks. This method represents a significant advancement in macromolecular cheminformatics, paving the way for the development of advanced search engines and data-driven design of macromolecules.

Key features include:
- **Pairwise Graph Similarity
- **LandMark Distance Embeddings

This repository provides all the datasets and scripts to reproduce all the results in the MacroSimGNN manuscript.
 
## Dataset

The [Dataset](./Dataset/) folder contains all the necessary graph data and graph edit distance data.

The [GED_Dataset_Visualization.ipynb](./Dataset/GED_Dataset_Visualization.ipynb) notebook visualizes the graph data (number of nodes and number of edges) and the graph edit distance dataset, as referenced in Figure 3 of the main text.

The [Graph_Pairwise_Similarity_Calculation.ipynb](./Dataset/Graph_Similarity_Calculation/Graph_Pairwise_Similarity_Calculation.ipynb) notebook explains how to calculate the graph edit distance between two graph representations of macromolecules using the A* method, as well as how to compute graph similarity using graph kernel methods. We refer to and modify the source code from [GLAMOUR](https://github.com/learningmatter-mit/GLAMOUR). The detailed modification is described in [./Dataset/Graph_Similarity_Calculation/README.md](./Dataset/Graph_Similarity_Calculation/README.md)


## Model

The [Model](./Model/) folder contains the source code to run the MacroSimGNN model. To develop MacroSimGNN, we refer to and modify the source code from [SimGNN](https://github.com/benedekrozemberczki/SimGNN) to process macromolecule coarse-grained graph representations. The detailed modifications are described in [Model/README.md](./Model/README.md)

## Results

The [Results](./Results/) folder includes the following:

- **[performance](./Results/performance/):** Describes the performance of the MacroSimGNN model in predicting pairwise graph similarity
- **[performance_vs_size](./Results/performance_vs_size/):** Explains how the performance of the MacroSimGNN model changes with the size of the training dataset
- **[classification](./Results/classification/):** Provides Details on the landmark distance embedding method and how it is used to predict the immunogenicity class of macromolecules.


## Contact

Jiale Shi, PhD  

Postdoctoral Associate  

Department of Chemical Engineering 

Massachusetts Institute of Technology (MIT) 

Email: jialeshi@mit.edu  

GithubID: [shijiale0609](https://github.com/shijiale0609)  


## Please cite our work and star this repo if it helps your research
## How to cite

```
@article{shi2024macrosimgnn,
author = {Jiale Shi, Dylan J. Walsh, Runzhong Wang, Nathan J. Rebello, Bradley D. Olsen, Debra J. Audus},
title = {MacroSimGNN: Efficient and Accurate Calculation of Macromolecule Pairwise Similarity via Graph Neural Network},
journal = {ChemRxiv},
year = {2024},
}
```

**License**

- [GNU](https://github.com/shijiale0609/MacroSimGNN/blob/master/LICENSE)
