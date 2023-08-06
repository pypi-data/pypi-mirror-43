![logo](https://github.com/benmaier/netwulf/raw/master/img/logo_small.png)

# netwulf

This package provides an interface between [networkx](https://networkx.github.io/) Graph objects and
[Ulf Aslak's interactive web app](https://github.com/ulfaslak/network_styling_with_d3) for simple
and better network visualizations.

## Install

    pip install netwulf

Beware: `netwulf` only works with Python 3!

## Example

### Standard

Create a network and look at it

```python
import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(100,m=1)
visualize(G)
```

![visualization example](https://github.com/benmaier/netwulf/raw/master/img/BA_1.png)

### Config

It's possible to change the default settings which are

```python
default_config = {
  'Apply heat (wiggle)': False,
  'Charge strength': -10,
  'Center gravity': 0.1,
  'Link distance': 10,
  'Link width': 2,
  'Link alpha': 0.5,
  'Node size': 10, 
  'Node stroke size': 0.5,
  'Node size exponent': 0.5,
  'Link strength exponent': 0.1,
  'Link width exponent': 0.5,
  'Collision': False,
  'Node fill': '#16a085',
  'Node stroke': '#000000',
  'Link stroke': '#7c7c7c',
  'Label stroke': '#000000',
  'Show labels': False,
  'Zoom': 1.5,
  'Min. link weight %': 0,
  'Max. link weight %': 100
}
```

It's done like so:

```python
import networkx as nx
from netwulf import visualize

G = nx.barabasi_albert_graph(5000,m=1)
visualize(G,config={
        'Node size': 11,
        'Charge strength' : -0.8,
        'Link distance' : 10,
        'Link width' : 1,
        'Collision' : True,
    })
```

![visualization example](https://github.com/benmaier/netwulf/raw/master/img/BA_2.png)


### Attributes
Node attributes such as 'group' or 'size' that you define in your `networkx.Graph` are automatically visualized.

```Python
import networkx as nx
import community
from netwulf import visualize

G = nx.random_partition_graph([10,10,10],.25,.01)
bb = community.best_partition(G)  # dict of node-community pairs
nx.set_node_attributes(G, bb, 'group')

visualize(G)
```

![visualization example](https://github.com/benmaier/netwulf/raw/master/img/attributes_1.png)

## Dev notes

The JS base code in `/netwulf/js/` is a fork of 
[Ulf Aslak's interactive web app](https://github.com/ulfaslak/network_styling_with_d3). If this repository
is updated, change to `/netwulf/js/`, then do

```bash
git fetch upstream/master
git pull upstream/master
git merge upstream/master
git commit -m "merged"
git push
```
