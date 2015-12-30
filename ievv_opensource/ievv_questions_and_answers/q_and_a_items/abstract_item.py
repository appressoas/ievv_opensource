class AbstractParsedItem(object):
    def __init__(self, rawtext, linenumber):
        self.rawtext = rawtext
        self.linenumber = linenumber

    @classmethod
    def match(cls, rawtext):
        raise NotImplementedError()

    def __str__(self):
        return self.rawtext


class AbstractParsedItemWithChildren(AbstractParsedItem):
    @classmethod
    def match(cls, rawtext):
        pass

    def __init__(self, rawtext, linenumber):
        super(AbstractParsedItemWithChildren, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.introduction_paragraph = None
        self.parseditems = []

    def append_item(self, parseditem):
        self.parseditems.append(parseditem)

    def set_introduction_paragraph(self, paragraph):
        self.introduction_paragraph = paragraph


class AbstractParsedQuestionChildItem(AbstractParsedItem):
    @classmethod
    def match(cls, rawtext):
        pass

    def get_typeid(self):
        raise NotImplementedError()