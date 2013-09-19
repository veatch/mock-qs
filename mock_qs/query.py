from mock_qs.constants import LOOKUP_SEP
from mock_qs.exceptions import MockNotImplementedError


class MockFieldLookups(object):
    @classmethod
    def apply(cls, item, lookup, field, val):
        return getattr(cls, '_%s' % lookup)(item, field, val)

    @classmethod
    def matches(cls, item, key_parts, val):
        if len(key_parts) == 2:
            field, lookup = key_parts
            if cls.is_valid(lookup):
                if cls.apply(item, lookup, field, val):
                    return True
            else:
                raise MockNotImplementedError
        else:
            # Handling relation attribute filtering
            # (e.g. widget__name__in) not implemented.
            raise MockNotImplementedError
        return False

    @classmethod
    def is_valid(cls, lookup):
        return hasattr(cls, '_%s' % lookup)

    @classmethod
    def _contains(cls, item, field, val):
        if val in getattr(item, field):
            return True
        return False

    @classmethod
    def _exact(cls, item, field, val):
        if getattr(item, field) == val:
            return True
        return False

    @classmethod
    def _gt(cls, item, field, val):
        if getattr(item, field) > val:
            return True
        return False

    @classmethod
    def _gte(cls, item, field, val):
        if getattr(item, field) >= val:
            return True
        return False

    @classmethod
    def _in(cls, item, field, val):
        if getattr(item, field) in val:
            return True
        return False

    @classmethod
    def _lt(cls, item, field, val):
        if getattr(item, field) < val:
            return True
        return False

    @classmethod
    def _lte(cls, item, field, val):
        if getattr(item, field) <= val:
            return True
        return False

    @classmethod
    def _startswith(cls, item, field, val):
        if getattr(item, field).startswith(val):
            return True
        return False

    @classmethod
    def _range(cls, item, field, val):
        begin, end = val
        if begin < getattr(item, field) < end:
            return True
        return False


class MockQuerySet(object):
    def __init__(self, results):
        self._mock_qs_results = results
        self._mock_field_lookups = MockFieldLookups

    def __getitem__(self, key):
        return self._mock_qs_results[key]

    def __len__(self):
        return len(self._mock_qs_results)

    def all(self):
        return self

    def filter(self, **kwargs):
        results = []
        for item in self._mock_qs_results:
            for key, val in kwargs.iteritems():
                key_parts = key.split(LOOKUP_SEP)
                if len(key_parts) > 1:
                    if self._mock_field_lookups.matches(item, key_parts, val):
                        results.append(item)
                elif getattr(item, key) == val:
                    results.append(item)
        return MockQuerySet(results)


class DjangoQuerySet(MockQuerySet):
    pass


class HaystackResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class HaystackQuerySet(MockQuerySet):
    pass
