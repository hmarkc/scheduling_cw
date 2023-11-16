# Initially, the method forms a VNS neighborhood Ni(x) around x, with i = 1. In the next
# step, called shaking, a random point y ∈ Ni(x) is chosen. If y ∈ Ni(x) is no better than x
# (g(y) ≥ g(x)), the VNS neighbourhood is expanded into Ni+1(x), such that Ni(x) ⊂ Ni+1(x),
# and the shaking step is executed again. Continuing in this fashion, if we cannot find a
# better solution after i exceeds a maximum value I, corresponding to the largest possible
# neighbourhood NI (x), we move to the next iteration k, revisiting the neighbourhoods from
# i = 1, but potentially obtaining different results due to randomisation in the shaking step.
# Once k exceeds the maximum number of iterations K, VNS returns the current solution x.
# In your code, assume NI (x) to coincide with the entire search space of feasible schedules

import random
from typing import Callable, List, Tuple
from utils import total_weighted_tardiness
from dag import DAG
from functools import partial
from tabu import Tabu

def neighborhood_by_swap(current_schedule: List[int], i: int, G: DAG) -> List[int]:
  """Generates a neighborhood of schedules

  Args:
      current_schedule (List[int]): 
        the current schedule of jobs, where the index of the job in the list is the job number minus one
      i (int): 
        the index of the neighborhood

  Returns:
      List[int]: 
        the randomly selected neighborhood of schedules
  """
  new_schedule = current_schedule.copy()
  count = 0
  while count < i:
    x = random.randint(0, len(new_schedule)-1)
    y = random.randint(0, x)
    valid = True
    for j in range(y, x+1):
      if G[new_schedule[y], new_schedule[j]] == 1 or G[new_schedule[j], new_schedule[x]] == 1:
        valid = False
        break
    if not valid:
      continue
    new_schedule[x], new_schedule[y] = new_schedule[y], new_schedule[x]
    count += 1
  return new_schedule

class RVNS(object):
  def __init__(self, neighborhood: Callable[[List[int], int, int, DAG], List[int]], max_I: int, seed: int) -> None:
    """Initializes the RVNS algorithm

    Args:
        neighborhood (Callable[[List[int], int, int, DAG], List[int]]): 
          the neighborhood function
        max_I (int): 
          the maximum number of iterations for each neighborhood
        seed (int): 
          the seed to use for random number generation
    """
    self._neighborhood = neighborhood
    self._max_I = max_I
    self._seed = seed
    self.check_points = []
  
  def rvns_search(self, intial_schedule: List[int], processing_times: List[float], due_dates: List[float], weights: List[float], K: int, G: DAG = DAG(), debug: int=0, optimization=False) -> Tuple[List[int], float]:
    """Runs the RVNS algorithm

    Args:
        intial_schedule (List[int]): 
          the initial schedule of jobs, where the index of the job in the list is the job number minus one
        processing_times (List[float]): 
          the processing time of each job, where the index of the job in the list is the job number minus one
        due_dates (List[float]): 
          the due date of each job, where the index of the job in the list is the job number minus one
        weights (List[float]): 
          the weight of each job, where the index of the job in the list is the job number minus one
        K (int): 
          the maximum number of iterations
        G (DAG, optional): 
          the directed acyclic graph of the jobs. Defaults to DAG().
        debug (int, optional): 
          the debug level. Defaults to 0.
        optimization (bool, optional):
          whether to optimize the schedule by local search. Defaults to False.

    Returns:
        Tuple[List[int], float]: 
          the best schedule found and its cost
    """
    random.seed(self._seed)
    self.check_points = []
    cost_fn = partial(total_weighted_tardiness, processing_times=processing_times, due_dates=due_dates, weights=weights)
    current_schedule = intial_schedule
    current_cost = cost_fn(current_schedule)
    k = 0
    tabu = None 
    if optimization:
      tabu = Tabu(L=self._max_I, gamma=0)
    while k < K:
      debug_msg = ''
      if debug > 0:
        debug_msg = f'k: {k}, current_cost: {current_cost}'
      if debug > 1:
        debug_msg += f', current_schedule: {current_schedule}'
      if debug_msg:
        print(debug_msg)
      i = 1
      while i <= self._max_I:
        new_schedule = self._neighborhood(current_schedule, i, G)
        new_cost = cost_fn(new_schedule)
        if optimization:
          new_schedule, new_cost = tabu.tabu_search(new_schedule, processing_times, due_dates, weights, G=G, K=i)
        if new_cost < current_cost:
          current_schedule = new_schedule
          current_cost = new_cost
          self.check_points.append((current_schedule, current_cost, k, i))
          break 
        i += 1
      k += 1
    self.check_points.append((current_schedule, current_cost, K, 0))
    return current_schedule, current_cost

