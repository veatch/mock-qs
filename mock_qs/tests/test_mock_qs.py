import pytest

from mock_qs.exceptions import MockNotImplementedError
from mock_qs.query import MockQuerySet

class FooClass(object):
    def __init__(self, name):
        self.name = name

class TestMockQuerySet(object):
    def setup(self):
        self.foo = FooClass(name='foo')
        self.bar = FooClass(name='bar')
        self.qs = MockQuerySet([self.foo, self.bar])

    def test_results(self):
        assert self.qs._results == [self.foo, self.bar]

    def test_filter(self):
        result = self.qs.filter(name='foo')
        assert result._results == [self.foo]

    def test_filter_in(self):
        result = self.qs.filter(name__in=['foo', 'buzz'])
        assert result._results == [self.foo]

    def test_bad_lookup(self):
        """
        A field lookup that isn't in LOOKUP_TERMS should raise an exception.
        """
        with pytest.raises(MockNotImplementedError):
            self.qs.filter(name__innnnnn=['foo'])

    def test_unknown_field(self):
        with pytest.raises(AttributeError):
            self.qs.filter(unknown_field='')

    def test_filter_chain(self):
        result = self.qs.filter(name='foo').filter(name='bar')
        assert result._results == []

    def test_filter_redundant_chain(self):
        result = self.qs.filter(name='foo').filter(name='foo')
        assert result._results == [self.foo]

    def test_relation_attribute(self):
        """
        Django-style access to a related objects's fields isn't
        supported yet.
        """
        with pytest.raises(MockNotImplementedError):
            self.qs.filter(site__id__in=[1])

    def test_len(self):
        assert len(self.qs) == 2
