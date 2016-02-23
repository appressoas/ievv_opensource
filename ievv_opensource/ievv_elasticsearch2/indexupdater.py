
class IndexUpdater(object):
    def __init__(self, doctype_class=None):
        self.doctype_class = doctype_class

    def reindex(self, obj):
        raise NotImplementedError()

    def reindex_all(self):
        self.reindex_all_with_high_priority()
        self.reindex_all_with_low_priority()

    def reindex_all_with_high_priority(self):
        raise NotImplementedError()

    def reindex_all_with_low_priority(self):
        pass
