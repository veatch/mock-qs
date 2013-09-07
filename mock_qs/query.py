class MockQuerySet(object):
    def __init__(self, results):
        self.results = results

    def filter(self, **kwargs): # ever just args?
        return [r for r in self.results if [k for k, v in kwargs.iteritems() if getattr(r, k, None) == v]]

# methods should accept result input and default to set.results if None ?
# to allow chaining

# keep filter, exclude, etc in parent and have django- and solr-specific
# queries in subclasses

# 'instance needs to have a primary key value before a many-to-many relationship can be used'
# how does factory boy handle this?

class DjangoQuerySet(MockQuerySet):
    pass

class HaystackQuerySet(MockQuerySet):
    pass
