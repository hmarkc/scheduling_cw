from dag import DAG
from tabu import Tabu
from rvns import RVNS, neighborhood_by_swap
from typing import List
import os 
import argparse

def workflow() -> DAG:
  G = DAG()
  with open(os.path.join('data', 'workflow.txt'), 'r') as f:
    for line in f:
      x, y = line.split(',')
      G[int(x), int(y)] = 1
  return G

def theo_due_dates() -> List[float]:
  d = []
  with open(os.path.join('data', 'theo_due_dates.csv'), 'r') as f:
    lines = [line for line in f]
    d = [0 for _ in lines]
    for line in lines:
      index, due = line.split(',')
      d[int(index)-1] = float(due)
  return d

def theo_processing_times() -> List[float]:
  p = []
  with open(os.path.join('data', 'theo_processing_times.csv'), 'r') as f:
    lines = [line for line in f]
    p = [0 for _ in lines]
    for line in lines:
      index, proc = line.split(',')
      p[int(index)-1] = float(proc)
  return p

if __name__ == '__main__':
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-method', type=str, default='tabu', help='the method to use: tabu or rvns')
  argparser.add_argument('-env', type=str, default='theo', help='the environment to use: theo or vm')
  argparser.add_argument('-L', type=int, default=20, help='the length of the tabu list')
  argparser.add_argument('-gamma', type=float, default=10, help='the gamma parameter')
  argparser.add_argument('-K', type=int, default=1000000, help='the number of iterations to run the algorithm for')
  argparser.add_argument('-debug', type=int, default=0, help='the level of debug messages to print')
  argparser.add_argument('-seed', type=int, default=0, help='the seed to use for random number generation')
  args = argparser.parse_args()

  G = workflow()
  G.save_fig('workflow.png')
  initial_schedule = [30, 29, 23, 10, 9, 14, 13, 12, 4, 20, 22, 3, 27, 28, 8, 7, 19, 21, 26, 18, 25, 17, 15, 6, 24, 16, 5, 11, 2, 1, 31]
  w = [1 for _ in range(31)]

  if args.env == 'theo':
    p = theo_processing_times()
    d = theo_due_dates()
  elif args.env == 'vm':
    # TODO: add vm data
    pass 
  else:
    raise ValueError(f'Invalid environment: {args.env}')

  if args.method == 'tabu':
    # Expected when K=1000000: [30, 20, 4, 3, 10, 14, 9, 8, 19, 23, 22, 21, 18, 7, 6, 17, 16, 29, 28, 27, 26, 25, 24, 13, 12, 5, 2, 15, 11, 1, 31]
    tabu = Tabu(L=args.L, gamma=args.gamma)
    print(tabu.tabu_search(initial_schedule, p, d, w, G=G, K=args.K, debug=args.debug))
  elif args.method == 'rvns':
    rvns = RVNS(neighborhood_by_swap, max_I=len(initial_schedule)-1, seed=args.seed)
    print(rvns.rvns_search(initial_schedule, p, d, w, G=G, K=args.K, debug=args.debug))
  else:
    raise ValueError(f'Invalid method: {args.method}')




