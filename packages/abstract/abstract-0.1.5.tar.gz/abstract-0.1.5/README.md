# Abstract
Abstract is a Python library for creating and drawing graphs 
and taking advantage of graph properties.

## Installation

```bash
pip install abstract
```
or
```bash
pip install git+https://github.com/idin/abstract.git
```


## Graph

In computer science, a graph is an abstract data type that 
is meant to implement the undirected graph and directed graph 
concepts from mathematics; specifically, the field of graph theory. 
[[1]](https://en.wikipedia.org/wiki/Graph_(abstract_data_type))

A graph data structure consists of a finite (and possibly mutable) 
set of vertices or nodes or points, together with a set of 
unordered pairs of these vertices for an undirected graph or 
a set of ordered pairs for a directed graph. These pairs are known 
as edges, arcs, or lines for an undirected graph and as arrows, 
directed edges, directed arcs, or directed lines for a directed graph. 
The vertices may be part of the graph structure, or may be external 
entities represented by integer indices or references. 
[[1]](https://en.wikipedia.org/wiki/Graph_(abstract_data_type))

## Usage

The *Graph* class allows you to create nodes and edges and 
visualize the resulting graph. Edges can have direction which
indicates parent-child relationship.

### *Graph*: Constructing a New Graph
```python
from abstract import Graph

graph = Graph()
```

### *add_node*: Adding a New Node
The *add_node* method returns a *GraphNode* object. 

```python
node_order = [
    'scissors', 'paper', 'rock', 'lizard', 'Spock', 'scissors',
    'lizard', 'paper', 'Spock', 'rock', 'scissors'
]

# add nodes (avoid duplicates)
for node in set(node_order):
    node = graph.add_node(name=node)
```

### *connect*: Adding Edges
The *connect* method creates an edge from a *start* node to an *end* node. 

```python
for index in range(len(node_order)-1):
    edge = graph.connect(start=node_order[index], end=node_order[index+1])
```

### *get_node*
To retrieve a node from the graph you can use the *get_node* method.
```python
rock = graph.get_node('rock')
```

### *draw* (*render*)
The *render* method visualizes the graph and if a *path* is provided it saves it
to an image file that can be a *pdf* or *png*. The file format is infered from 
the *path* argument. The *draw* method is just an alias for *render*.

```python
# just visualize the graph
graph.draw()
```
![image of the graph](https://raw.githubusercontent.com/idin/abstract/master/pictures/rock_paper.png)


```python
# save as a png file and view the file
graph.draw(path='my_graph.png', view=True)

```

## Future Features

* Create a graph from:
  * list of dictionaries
  * dataframe
* Create a new graph by filtering a graph
