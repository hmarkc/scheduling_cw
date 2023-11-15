import unittest
from tabu import * 

class TestTabu(unittest.TestCase):

  def test_t3_p7(self):
    w = [14, 12, 1, 12]
    d = [4, 2, 1, 12]
    p = [10, 10, 13, 4]
    tabu = Tabu(L=2, gamma=100)
    self.assertEqual(tabu.tabu_search([2, 1, 4, 3], p, d, w, K=3, debug=4), ([1, 4, 2, 3], 408))



if __name__ == '__main__':
    unittest.main()

