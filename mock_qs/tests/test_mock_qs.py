import datetime
import pytest

from mock_qs.exceptions import MockNotImplementedError
from mock_qs.query import MockQuerySet

class FooClass(object):
    def __init__(self, name):
        self.name = name

class DateClass(object):
    def __init__(self, dt):
        self.dt = dt

class TestMockQuerySet(object):
    def setup(self):
        self.foo = FooClass(name='foo')
        self.bar = FooClass(name='bar')
        self.qs = MockQuerySet([self.foo, self.bar])

    def test_mock_qs_results(self):
        assert self.qs._mock_qs_results == [self.foo, self.bar]

    def test_slice(self):
        assert self.qs[0] == self.foo
        assert self.qs[1] == self.bar

    def test_all_len_list(self):
        assert len(self.qs.all()) == 2
        assert list(self.qs.all()) == [self.foo, self.bar]

    def test_all_slice(self):
        assert self.qs.all()[0] == self.foo
        assert self.qs.all()[1] == self.bar

    def test_filter(self):
        result = self.qs.filter(name='foo')
        assert result._mock_qs_results == [self.foo]

    def test_filter_in(self):
        result = self.qs.filter(name__in=['foo', 'buzz'])
        assert result._mock_qs_results == [self.foo]

    def test_filter_contains(self):
        result = self.qs.filter(name__contains='f')
        assert result._mock_qs_results == [self.foo]

    def test_filter_exact(self):
        self.qs._mock_qs_results.append(FooClass(name='fooooooo'))
        result = self.qs.filter(name__exact='foo')
        assert result._mock_qs_results == [self.foo]

    def test_filter_startswith(self):
        self.fooooooo = FooClass(name='fooooooo')
        self.qs._mock_qs_results.append(self.fooooooo)
        result = self.qs.filter(name__startswith='foo')
        assert result._mock_qs_results == [self.foo, self.fooooooo]

    def test_bad_lookup(self):
        with pytest.raises(MockNotImplementedError):
            self.qs.filter(name__innnnnn=['foo'])

    def test_unknown_field(self):
        with pytest.raises(AttributeError):
            self.qs.filter(unknown_field='')

    def test_filter_chain(self):
        result = self.qs.filter(name='foo').filter(name='bar')
        assert result._mock_qs_results == []

    def test_filter_redundant_chain(self):
        result = self.qs.filter(name='foo').filter(name='foo')
        assert result._mock_qs_results == [self.foo]

    def test_relation_attribute(self):
        """
        Django-style access to a related objects's fields isn't
        supported yet.
        """
        with pytest.raises(MockNotImplementedError):
            self.qs.filter(site__id__in=[1])

    def test_len(self):
        assert len(self.qs) == 2


class TestDatetimeFieldLookups(object):
    def setup(self):
        self.foo = DateClass(dt=datetime.datetime(2013, 9, 1, 0, 0))
        self.bar = DateClass(dt=datetime.datetime(2013, 9, 19, 0, 0))
        self.buzz = DateClass(dt=datetime.datetime(2014, 2, 1, 0, 0))
        self.qs = MockQuerySet([self.foo, self.bar, self.buzz])

    def test_datetime_filter_gt(self):
        result = self.qs.filter(dt__gt=datetime.datetime(2013, 9, 19, 0, 0))
        assert result._mock_qs_results == [self.buzz]

    def test_datetime_filter_gte(self):
        result = self.qs.filter(dt__gte=datetime.datetime(2013, 9, 19, 0, 0))
        assert result._mock_qs_results == [self.bar, self.buzz]

    def test_datetime_filter_lt(self):
        result = self.qs.filter(dt__lt=datetime.datetime(2013, 9, 19, 0, 0))
        assert result._mock_qs_results == [self.foo]

    def test_datetime_filter_lte(self):
        result = self.qs.filter(dt__lte=datetime.datetime(2013, 9, 19, 0, 0))
        assert result._mock_qs_results == [self.foo, self.bar]

    def test_datetime_filter_range(self):
        result = self.qs.filter(dt__range=(datetime.datetime(2013, 9, 18, 0, 0), datetime.datetime(2013, 9, 20, 0, 0)))
        assert result._mock_qs_results == [self.bar]
