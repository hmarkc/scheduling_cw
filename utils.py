from typing import List
from dag import DAG
import os 

def total_weighted_tardiness(schedule: List[int], processing_times: List[float], due_dates: List[float], weights: List[float]) -> float:
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

def workflow() -> DAG:
  G = DAG()
  with open(os.path.join('data', 'workflow.txt'), 'r') as f:
    for line in f:
      x, y = line.split(',')
      G[int(x), int(y)] = 1
  return G

def due_dates() -> List[float]:
  d = []
  with open(os.path.join('data', 'theo_due_dates.csv'), 'r') as f:
    lines = [line for line in f]
    d = [0 for _ in lines]
    for line in lines:
      index, due = line.split(',')
      d[int(index)-1] = float(due)
  return d

def processing_times(vm: bool = False) -> List[float]:
  p = []
  file = 'vm_processing_times.csv' if vm else 'theo_processing_times.csv'
  with open(os.path.join('data', file), 'r') as f:
    lines = [line for line in f]
    p = [0 for _ in lines]
    for line in lines:
      index, proc = line.split(',')
      p[int(index)-1] = float(proc)
  return p