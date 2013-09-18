from mock_qs.constants import LOOKUP_SEP, LOOKUP_TERMS
from mock_qs.exceptions import MockNotImplementedError


class MockQuerySet(object):
    def __init__(self, results):
        self._results = results

    def __len__(self):
        return len(self._results)

    def filter(self, **kwargs):
        results = []
        for res in self._results:
            for key, val in kwargs.iteritems():
                key_parts = key.split(LOOKUP_SEP)
                if len(key_parts) > 1:
                    if len(key_parts) == 2:
                        field, lookup = key_parts
                        if lookup in LOOKUP_TERMS:
                            if getattr(res, field) in val:
                                results.append(res)
                        else:
                            raise MockNotImplementedError
                    else:
                        raise MockNotImplementedError
                elif getattr(res, key) == val:
                    results.append(res)
        return MockQuerySet(results)


class DjangoQuerySet(MockQuerySet):
    pass


class HaystackResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class HaystackQuerySet(MockQuerySet):
    pass
