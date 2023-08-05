import unittest

from pimpygui.history_stack import HistoryStack


class TestHistoryStack(unittest.TestCase):

    def test_no_arg_constructor(self):
        s = HistoryStack()
        self.assertEqual(len(s), 0)
        self.assertEqual(list(s), [])
        self.assertEqual(s.get_current_index(), -1)

    def test_single_arg_constructor(self):
        s = HistoryStack([2, "hello", True])
        self.assertEqual(len(s), 3)
        self.assertEqual(list(s), [2, "hello", True])
        self.assertEqual(s.get_current_index(), -1)

    def test_two_arg_constructor(self):
        s = HistoryStack([2, "hello", True], 1)
        self.assertEqual(len(s), 3)
        self.assertEqual(list(s), [2, "hello", True])
        self.assertEqual(s.get_current_index(), 1)

    def test_two_arg_constructor_clips_min_index(self):
        s = HistoryStack([2, "hello", True], -5)
        self.assertEqual(len(s), 3)
        self.assertEqual(list(s), [2, "hello", True])
        self.assertEqual(s.get_current_index(), -1)

    def test_two_arg_constructor_clips_max_index(self):
        s = HistoryStack([2, "hello", True], 5)
        self.assertEqual(len(s), 3)
        self.assertEqual(list(s), [2, "hello", True])
        self.assertEqual(s.get_current_index(), 2)

    def test_list_in_constructor_is_not_shared(self):
        a = [2, "hello", True]
        s = HistoryStack(a)
        a.pop()
        self.assertEqual(list(s), [2, "hello", True])

    def test_get_elements(self):
        s = HistoryStack([2, "hello", True], -1)
        self.assertIsNone(s.get())
        s = HistoryStack([2, "hello", True], 0)
        self.assertEqual(s.get(), 2)
        s = HistoryStack([2, "hello", True], 1)
        self.assertEqual(s.get(), "hello")
        s = HistoryStack([2, "hello", True], 2)
        self.assertEqual(s.get(), True)

    def test_add_to_empty(self):
        s = HistoryStack()
        s.add(2)
        self.assertEqual(len(s), 1)
        self.assertEqual(list(s), [2])
        self.assertEqual(s.get_current_index(), 0)
        self.assertEqual(s.get(), 2)

    def test_add_to_non_empty_at_begin(self):
        s = HistoryStack([2, "hello", True], -1)
        s.add(5)
        self.assertEqual(len(s), 1)
        self.assertEqual(list(s), [5])
        self.assertEqual(s.get_current_index(), 0)
        self.assertEqual(s.get(), 5)

    def test_add_to_non_empty_at_middle(self):
        s = HistoryStack([2, "hello", True], 0)
        s.add(5)
        self.assertEqual(len(s), 2)
        self.assertEqual(list(s), [2, 5])
        self.assertEqual(s.get_current_index(), 1)
        self.assertEqual(s.get(), 5)

    def test_add_to_non_empty_at_end(self):
        s = HistoryStack([2, "hello", True], 2)
        s.add(5)
        self.assertEqual(len(s), 4)
        self.assertEqual(list(s), [2, "hello", True, 5])
        self.assertEqual(s.get_current_index(), 3)
        self.assertEqual(s.get(), 5)

    def test_can_go_backwards_forwards_left(self):
        s = HistoryStack([2, "hello", True], -1)
        self.assertFalse(s.can_go_backwards())
        self.assertTrue(s.can_go_forwards())

    def test_can_go_backwards_forwards_middle_0(self):
        s = HistoryStack([2, "hello", True], 0)
        self.assertTrue(s.can_go_backwards())
        self.assertTrue(s.can_go_forwards())

    def test_can_go_backwards_forwards_middle_1(self):
        s = HistoryStack([2, "hello", True], 1)
        self.assertTrue(s.can_go_backwards())
        self.assertTrue(s.can_go_forwards())

    def test_can_go_backwards_forwards_right(self):
        s = HistoryStack([2, "hello", True], 2)
        self.assertTrue(s.can_go_backwards())
        self.assertFalse(s.can_go_forwards())

    def test_go_backwards_left(self):
        s = HistoryStack([2, "hello", True], -1)
        s.go_backwards()
        self.assertEqual(s.get_current_index(), -1)
        self.assertIsNone(s.get())

    def test_go_forwards_left(self):
        s = HistoryStack([2, "hello", True], -1)
        s.go_forwards()
        self.assertEqual(s.get_current_index(), 0)
        self.assertEqual(s.get(), 2)

    def test_go_backwards_middle(self):
        s = HistoryStack([2, "hello", True], 0)
        s.go_backwards()
        self.assertEqual(s.get_current_index(), -1)
        self.assertIsNone(s.get())

    def test_go_forwards_middle(self):
        s = HistoryStack([2, "hello", True], 0)
        s.go_forwards()
        self.assertEqual(s.get_current_index(), 1)
        self.assertEqual(s.get(), "hello")

    def test_go_backwards_right(self):
        s = HistoryStack([2, "hello", True], 2)
        s.go_backwards()
        self.assertEqual(s.get_current_index(), 1)
        self.assertEqual(s.get(), "hello")

    def test_go_forwards_right(self):
        s = HistoryStack([2, "hello", True], 2)
        s.go_forwards()
        self.assertEqual(s.get_current_index(), 2)
        self.assertEqual(s.get(), True)
