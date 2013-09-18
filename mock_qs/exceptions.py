class MockNotImplementedError(Exception):
    """
    Custom NotImplementedError for when user tries something
    that's valid in Django/Haystack but unimplemented in mock-qs.
    """
    pass
