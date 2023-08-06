from qc_utils import QCMetric, QCMetricRecord
from unittest import TestCase
from collections import OrderedDict


class TestQCMetric(TestCase):
    def setUp(self):
        self.ordered = OrderedDict([(2, 'a'), (1, 'b')])

    def test_type_check(self):
        with self.assertRaises(TypeError):
            QCMetric('name', 1)

    def test_get_name(self):
        qc_obj = QCMetric('a', {})
        self.assertEqual(qc_obj.name, 'a')

    def test_get_content(self):
        qc_obj = QCMetric('_', {2: 'a', 1: 'b'})
        self.assertEqual(qc_obj.content, OrderedDict([(1, 'b'), (2, 'a')]))

    def test_less_than(self):
        smaller_obj = QCMetric(1, {})
        bigger_obj = QCMetric(2, {})
        self.assertTrue(smaller_obj < bigger_obj)

    def test_equals(self):
        first_obj = QCMetric('a', {})
        second_obj = QCMetric('a', {'x': 'y'})
        self.assertTrue(first_obj == second_obj)

    def test_repr(self):
        obj = QCMetric('a', {1: 'x'})
        self.assertEqual(obj.__repr__(),
                         "QCMetric('a', OrderedDict([(1, 'x')]))")

    def test_retains_order_when_created_from_OrderedDict(self):
        qc_obj = QCMetric('name', self.ordered)
        self.assertEqual(qc_obj.content, self.ordered)


class TestQCMetricRecord(TestCase):
    def setUp(self):
        self.obj_a1 = QCMetric('a', {1: 2})
        self.obj_a2 = QCMetric('a', {2: 3})
        self.obj_b = QCMetric('b', {3: 4})
        self.obj_c = QCMetric('c', {1: 2, 3: 4, 5: 6})
        self.obj_d = QCMetric('d', {'a': 'b'})
        self.qc_record = QCMetricRecord()

    def test_init_from_list_not_unique(self):
        metrics = [self.obj_a1, self.obj_a2]
        with self.assertRaises(AssertionError):
            QCMetricRecord(metrics)

    def test_init_from_list_success(self):
        metrics = [self.obj_a1, self.obj_b]
        record = QCMetricRecord(metrics)
        self.assertEqual(record.metrics[0], self.obj_a1)
        self.assertEqual(record.metrics[1], self.obj_b)

    def test_add(self):
        self.assertEqual(len(self.qc_record), 0)
        self.qc_record.add(self.obj_a1)
        self.assertEqual(len(self.qc_record), 1)

    def test_add_all_to_empty(self):
        metrics = [self.obj_a1, self.obj_b]
        self.qc_record.add_all(metrics)
        self.assertEqual(len(self.qc_record), 2)

    def test_add_all_to_nonempty_success(self):
        metrics = [self.obj_a1, self.obj_b]
        record = QCMetricRecord(metrics)
        record.add_all([self.obj_c, self.obj_d])
        self.assertEqual(len(record), 4)

    def test_add_all_failure_because_not_unique(self):
        record = QCMetricRecord([self.obj_a1])
        with self.assertRaises(AssertionError):
            record.add_all([self.obj_b, self.obj_a2])
        self.assertEqual(len(record), 1)

    def test_add_raises_error_when_add_same_twice(self):
        self.qc_record.add(self.obj_a1)
        with self.assertRaises(AssertionError):
            self.qc_record.add(self.obj_a1)

    def test_add_raises_error_when_add_with_same_name(self):
        self.qc_record.add(self.obj_a1)
        with self.assertRaises(AssertionError):
            self.qc_record.add(self.obj_a2)

    def test_to_ordered_dict(self):
        self.qc_record.add(self.obj_a1)
        self.qc_record.add(self.obj_b)
        qc_dict = self.qc_record.to_ordered_dict()
        self.assertEqual(qc_dict, OrderedDict([('a', {1: 2}), ('b', {3: 4})]))

    def test_repr(self):
        metrics = [self.obj_a1, self.obj_b]
        record = QCMetricRecord(metrics)
        self.assertEqual(record.__repr__(),
                         "QCMetricRecord([QCMetric('a', OrderedDict([(1, 2)])), QCMetric('b', OrderedDict([(3, 4)]))])")
