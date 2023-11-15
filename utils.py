from typing import List

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