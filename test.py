import unittest
from tabu import * 

class TestTabu(unittest.TestCase):

  def test_t3_p7(self):
    w = [14, 12, 1, 12]
    d = [4, 2, 1, 12]
    p = [10, 10, 13, 4]
    tabu = Tabu(L=2, gamma=100)
    self.assertEqual(tabu.tabu_search([2, 1, 4, 3], p, d, w, K=3, debug=4), ([1, 4, 2, 3], 408))
  
  def test_t3_p8(self):
    w = [3, 4, 5, 7]
    d = [1, 2, 7, 9]
    p = [16, 11, 4, 8]
    tabu = Tabu(L=2, gamma=20)
    self.assertEqual(tabu.tabu_search([4, 2, 1, 3], p, d, w, K=4, debug=4), ([3, 4, 2, 1], 219))



if __name__ == '__main__':
    unittest.main()

