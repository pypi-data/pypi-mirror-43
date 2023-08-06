from bisect import insort
from collections import OrderedDict


class QCMetric(object):
    """Container that holds the qc metric as OrderedDict (sorted by keys of
    the input dict) and the "master" key (name) of the said qc metric. Can be
    instantiated from a regular dict.
    If you want a custom order of items, instantiate from an OrderedDict
    to skip sorting by keys and keep the original order (or pass a parser
    that returns an OrderedDict instead of a vanilla one).
    """

    def __init__(self, qc_metric_name, qc_metric_content, parser=None):
        if parser is not None:
            qc_metric_dict = parser(qc_metric_content)
        else:
            qc_metric_dict = qc_metric_content
        if not isinstance(qc_metric_dict, dict):
            raise TypeError('QCMetric data must be a dict.')
        self._name = qc_metric_name
        if isinstance(qc_metric_dict, dict) and not isinstance(qc_metric_dict, OrderedDict):
            self._content = OrderedDict(
                sorted(qc_metric_dict.items(), key=lambda x: x[0]))
        else:
            self._content = OrderedDict(qc_metric_dict)

    @property
    def content(self):
        return self._content

    @property
    def name(self):
        return self._name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return 'QCMetric(%r, %r)' % (self.name, self.content)


class QCMetricRecord(object):
    """Container that holds QCMetrics in sorted order.

    Attributes:
        metrics: list of metrics, kept sorted by the name of metrics
    """

    def __init__(self, metrics=None):
        if metrics is None:
            self._metrics = []
        else:
            # names must be unique
            names = [metric.name for metric in metrics]
            assert len(names) == len(
                set(names)), 'Names of metrics have to be unique'
            metrics.sort()
            self._metrics = metrics

    @property
    def metrics(self):
        return self._metrics

    def add(self, qc_metric):
        """Adds qc metric to the metrics, keeping it sorted by name.

        Args:
            qc_metric: QCMetric

        Returns: None

        Raises: AssertionError if a metric with same name is already in record
        """

        assert qc_metric not in self._metrics, 'Metric with name {} already in record'.format(
            qc_metric.name)
        insort(self._metrics, qc_metric)

    def add_all(self, qc_metric_container):
        """Adds all metrics from qc_metric_container preserving uniquness of names and order.
        If the names in the qc_metric_container are not unique, raises AssertionError and leaves
        the QCMetricRecord unmodified.
        Args:
            qc_metric_container: list (or a container that can be converted into a list) of QCMetrics
        Returns: None

        Raises: AssertionError if adding would break the uniqueness of names in self.
        """
        qc_metric_list = list(qc_metric_container)
        for metric in qc_metric_list:
            assert metric not in self._metrics, 'Metric with name {} already in record. Nothing from the container added'.format(
                metric.name)
        for metric in qc_metric_list:
            self.add(metric)

    def to_ordered_dict(self):
        """Returns an OrderedDict with the contents.

        Returns: Ordered dict with structure as follows:
            - Ordered as the metrics is
            - Contents, assuming metrics = [qc1, qc2, qc3]:
            {
                qc1.name : qc1.content,
                qc2.name : qc2.content,
                qc3.name : qc3.content
            }
        """
        result = OrderedDict()
        for metric in self.metrics:
            result.update({metric.name: metric.content})
        return result

    def __len__(self):
        """
        Delegated to metrics.
        """
        return len(self.metrics)

    def __iter__(self):
        """
        Iterating QCMetricRecord is iterating over metrics.
        """
        return iter(self.metrics)

    def __repr__(self):
        """
        Like __iter__, __repr__ is delegated to metrics.
        """
        return 'QCMetricRecord(%s)' % self.metrics.__repr__()
