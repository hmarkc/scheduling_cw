from typing import Tuple, List
from collections import defaultdict
import networkx as nx
from matplotlib import pyplot as plt

class DAG(object):
  def __init__(self) -> None:
    self._dependencies = defaultdict(set)
    self._graph = nx.DiGraph()
  
  @property
  def edges(self) -> List[Tuple[int, int]]:
    return self._graph.edges()
  
  @property
  def nodes(self) -> List[int]:
    return self._graph.nodes()

  def _add_dependency(self, parent: int, child: int) -> None:
    self._dependencies[child].add(parent)
    for grandparent in self._dependencies[parent]:
      self._add_dependency(grandparent, child)
  
  def __setitem__(self, key: Tuple[int, int], value: int) -> None:
    assert value == 1
    parent, child = key
    self._graph.add_edge(parent, child)
    assert nx.is_directed_acyclic_graph(self._graph)
    self._add_dependency(parent, child)
  
  def __getitem__(self, key: Tuple[int, int]) -> int:
    x, y = key
    return 1 if x in self._dependencies[y] else 0 
  
  def save_fig(self, name) -> str:
    nx.draw_networkx(self._graph, arrows=True)
    plt.savefig(name, format="PNG")
    plt.clf()


    
