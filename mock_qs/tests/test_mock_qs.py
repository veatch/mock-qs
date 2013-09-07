from mock_qs.query import MockQuerySet

class FooClass(object):
    def __init__(self, name):
        self.name = name

def test_mock_qs():
    foo = FooClass(name='foo')
    bar = FooClass(name='bar')
    qs = MockQuerySet([foo, bar])
    result = qs.filter(name='foo')
    assert result == [foo]
