from dag import DAG
from tabu import Tabu
from typing import List
import os 

def q2_dac() -> DAG:
  G = DAG()
  with open(os.path.join('data', 'q2_dac.txt'), 'r') as f:
    for line in f:
      x, y = line.split(',')
      G[int(x), int(y)] = 1
  return G

def q2_due_dates() -> List[float]:
  d = []
  with open(os.path.join('data', 'q2_due_dates.csv'), 'r') as f:
    lines = [line for line in f]
    d = [0 for _ in lines]
    for line in lines:
      index, due = line.split(',')
      d[int(index)-1] = float(due)
  return d

def q2_processing_times() -> List[float]:
  p = []
  with open(os.path.join('data', 'q2_processing_times.csv'), 'r') as f:
    lines = [line for line in f]
    p = [0 for _ in lines]
    for line in lines:
      index, proc = line.split(',')
      p[int(index)-1] = float(proc)
  return p

if __name__ == '__main__':
  G = q2_dac()
  G.save_fig('q2_dac.png')
  p = q2_processing_times()
  d = q2_due_dates()
  initial_schedule = [30, 29, 23, 10, 9, 14, 13, 12, 4, 20, 22, 3, 27, 28, 8, 7, 19, 21, 26, 18, 25, 17, 15, 6, 24, 16, 5, 11, 2, 1, 31]
  w = [1 for _ in range(31)]
  tabu = Tabu(L=20, gamma=10)
  print(tabu.tabu_search(initial_schedule, p, d, w, G=G, K=500000, debug=4))




