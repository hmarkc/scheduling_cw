from typing import Tuple, List
from collections import defaultdict
import networkx as nx
from matplotlib import pyplot as plt

class DAG(object):
  """A class used to represent a directed acyclic graph

  Args:
  """
  def __init__(self) -> None:
    self._dependencies = defaultdict(set)
    self._dependents = defaultdict(set)
    self._graph = nx.DiGraph()
  
  @property
  def edges(self) -> List[Tuple[int, int]]:
    """Returns the edges of the graph

    Returns:
        List[Tuple[int, int]]:
          the edges of the graph 
    """
    return self._graph.edges()
  
  @property
  def nodes(self) -> List[int]:
    return self._graph.nodes()

  def _add_dependency(self, parent: int, child: int) -> None:
    """Adds a dependency between two jobs

    Args:
        parent (int): 
          the parent job
        child (int): 
          the child job
    """
    self._dependencies[child].add(parent)
    self._dependents[parent].add(child)
    for grandparent in self._dependencies[parent]:
      self._add_dependency(grandparent, child)
    for grandchild in self._dependents[child]:
      self._add_dependency(parent, grandchild)
  
  def __setitem__(self, key: Tuple[int, int], value: int) -> None:
    """Adds an edge between two jobs

    Args:
        key (Tuple[int, int]):
          the parent and child jobs
        value (int): 
          the value of the edge
    """
    assert value == 1
    parent, child = key
    self._graph.add_edge(parent, child)
    assert nx.is_directed_acyclic_graph(self._graph)
    self._add_dependency(parent, child)
  
  def __getitem__(self, key: Tuple[int, int]) -> int:
    """Returns the value of the edge between two jobs

    Args:
        key (Tuple[int, int]):
          the parent and child jobs

    Returns:
        int: 
          the value of the edge
    """
    x, y = key
    return 1 if x in self._dependencies[y] else 0 
  
  def check_valid(self, schedule: List[int]) -> bool:
    """Checks if a schedule is valid

    Args:
        schedule (List[int]): 
          the schedule of jobs, where the index of the job in the list is the job number minus one

    Returns:
        bool: 
          True if the schedule is valid, False otherwise
    """
    for i in range(len(schedule)):
      for j in range(i+1, len(schedule)):
        if self[schedule[j], schedule[i]] == 1:
          print(f'Invalid: {schedule[i]} depends on {schedule[j]}, {i}, {j}')
          return False
    return True

  def save_fig(self, name) -> str:
    """Saves the graph as a PNG

    Args:
        name (_type_): 
          the name of the file to save the graph to

    Returns:
        str:
          the name of the file the graph was saved to
    """
    nx.draw_networkx(self._graph, arrows=True)
    plt.savefig(name, format="PNG")
    plt.clf()
      