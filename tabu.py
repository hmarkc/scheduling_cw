# tabu search algorithm 
# In your implementation:
# • Make sure that your implementation is generic, i.e., it can accept an arbitrary set of
# processing times, due dates, and precedences (the latter can be assumed to form a
# directed acyclic graph). You can assume the initial schedule to be always valid.
# • Explore the local neighborhoods using the same rules used in the exercises of Problem
# Sheet 3, i.e., for a schedule 1234 if at iteration k you last considered adjacent interchange
# e.g. (2, 3), at iteration k + 1 consider first adjacent interchange (3, 4), then (1, 2), etc.
# • Compared to the tabu search algorithms seen in class, you will need to introduce in the
# generation of the neighborhood a strategy to account for job precedences.

from collections import deque
from typing import List, Tuple, Callable
from functools import partial

class Tabu(object):
  """
  A class used to represent the Tabu Search algorithm

  Attributes
  ----------
  L : int
    the length of the tabu list
  gamma : float
    the threshold value for the cost difference between the current solution and the new solution

  Methods
  -------
  _total_weighted_tardiness(schedule, processing_times, due_dates, weights)
    Calculates the total weighted tardiness of a schedule
  _swap_in_tabu_list(tabu_list, x1, x2)
    Checks if a swap is in the tabu list
  tabu_search(intial_schedule, processing_times, due_dates, weights, K, debug)
    Runs the tabu search algorithm
  """
  def __init__(self, L: int, gamma: float) -> None:
    """
    Parameters    
    ----------
    L : int
      the length of the tabu list
    gamma : float
      the threshold value for the cost difference between the current solution and the new solution
    """
    self.L = L 
    self.gamma = gamma

  def _total_weighted_tardiness(self, schedule: List[int], processing_times: List[float], due_dates: List[float], weights: List[float]) -> float:
    """Calculates the total weighted tardiness of a schedule

    Args:
        schedule (List[int]): 
          the schedule of jobs, where the index of the job in the list is the job number minus one
        processing_times (List[float]):
          the processing time of each job, where the index of the job in the list is the job number minus one
        due_dates (List[float]): 
          the due date of each job, where the index of the job in the list is the job number minus one
        weights (List[float]): 
          the weight of each job, where the index of the job in the list is the job number minus one

    Returns:
        float: 
          the total weighted tardiness of the schedule
    """
    tardiness = 0
    time = 0
    for i in schedule:
      job = i - 1
      time += processing_times[job]
      tardiness += max(0, time - due_dates[job]) * weights[job]
    return tardiness
  
  def _swap_in_tabu_list(self, tabu_list: List[Tuple[int, int]], x1: int, x2: int) -> bool:
    """Checks if a swap is in the tabu list

    Args:
        tabu_list (List[Tuple[int, int]]): 
          the tabu list, where each element is a tuple of two integers representing the job numbers
        x1 (int): 
          the first job number
        x2 (int): 
          the second job number

    Returns:
        bool: 
          True if the swap is in the tabu list, False otherwise
    """
    for pair in tabu_list:
      if (x1, x2) == pair or (x2, x1) == pair:
        return True
    return False

  def tabu_search(self, intial_schedule: List[int], processing_times: List[float], due_dates: List[float], weights: List[float], K: int, debug: int=0) -> Tuple[List[int], float]:
    """Runs the tabu search algorithm

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
          the number of iterations to run the algorithm for
        debug (int, optional): 
          the level of debug messages to print. Defaults to 0.

    Returns:
        Tuple[List[int], float]: 
          the best schedule of jobs and its total weighted tardiness
    """
    num_jobs = len(intial_schedule)
    assert num_jobs == len(processing_times) == len(due_dates) == len(weights)
    cost_fn = partial(self._total_weighted_tardiness, processing_times=processing_times, due_dates=due_dates, weights=weights)
    k = 0 
    current_schedule = intial_schedule
    best_schedule = current_schedule
    current_cost = cost_fn(current_schedule)
    best_cost = current_cost
    tabu_list = deque([], maxlen=self.L)
    last_swap_index = 0 # index of the second element in the last swap 

    while k <= K:
      debug_msg = ''
      if debug > 0:
        debug_msg = f'k: {k}, current_cost: {current_cost}, best_cost: {best_cost}'
      if debug > 1:
        debug_msg += f', current_schedule: {current_schedule}, best_schedule: {best_schedule}'
      if debug > 2:
        debug_msg += f', tabu_list: {tabu_list}'
      if debug_msg:
        print(debug_msg)
      i = last_swap_index
      while True: 
        new_schedule = current_schedule.copy()
        new_schedule[i], new_schedule[i + 1] = new_schedule[i + 1], new_schedule[i]
        new_cost = cost_fn(new_schedule)
        delta = current_cost - new_cost
        if (delta > -self.gamma and not self._swap_in_tabu_list(tabu_list, current_schedule[i], current_schedule[i + 1])) or new_cost < best_cost:
          tabu_list.append((current_schedule[i], current_schedule[i + 1]))
          if new_cost < best_cost:
            best_schedule = new_schedule
            best_cost = new_cost
          current_schedule = new_schedule
          current_cost = new_cost
          break
        i = (i + 1) % (num_jobs - 1)
        # if we have gone through all the possible swaps, then break
        if i == last_swap_index:
          break

      last_swap_index = (i + 1) % (num_jobs - 1)
      k += 1

    return best_schedule, best_cost

if __name__ == '__main__':
  tabu = Tabu(L=5, gamma=0.1)
  print(tabu.tabu_search([1, 2, 3, 4], [14, 12, 1, 12], [4, 2, 1, 12], [10, 10, 13, 4], K=100))

    
