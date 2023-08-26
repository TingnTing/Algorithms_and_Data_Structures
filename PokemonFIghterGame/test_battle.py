__author__ = "T06G06"

import unittest
from tester_base import captured_output
from battle import Battle


class TestBattle(unittest.TestCase):
  def test_set_mode_battle(self):
      b = Battle("p1", "p2")
      with captured_output("0 0 0\n0 0 0") as (inp, out, err):
        result = b.set_mode_battle()
        self.assertEqual(str(result),"Draw")

      with captured_output("1 0 0\n0 0 0") as (inp, out, err):
        result = b.set_mode_battle()
        self.assertEqual(str(result),"p1")

      with captured_output("0 0 0\n1 0 0") as (inp, out, err):
        result = b.set_mode_battle()
        self.assertEqual(str(result),"p2")

  def test_rotating_mode_battle(self):
    b = Battle("p1", "p2")
    with captured_output("0 0 0\n0 0 0") as (inp, out, err):
      result = b.rotating_mode_battle()
      self.assertEqual(str(result),"Draw")

    with captured_output("1 0 0\n0 0 0") as (inp, out, err):
      result = b.rotating_mode_battle()
      self.assertEqual(str(result),"p1")

    with captured_output("0 0 0\n1 0 0") as (inp, out, err):
      result = b.rotating_mode_battle()
      self.assertEqual(str(result),"p2")

if __name__ == '__main__':
    unittest.main()