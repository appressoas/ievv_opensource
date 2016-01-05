class AbstractParsedItem(object):
    """

    """
    def __init__(self, rawtext, linenumber):
        self.rawtext = rawtext
        self.linenumber = linenumber

    @classmethod
    def match(cls, rawtext):
        raise NotImplementedError()

    def get_typeid(self):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    def __str__(self):
        return self.rawtext


class AbstractParsedItemWithChildren(AbstractParsedItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        pass

    def __init__(self, rawtext, linenumber):
        super(AbstractParsedItemWithChildren, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.heading = rawtext[2:].strip()
        self.introduction_paragraph = None
        self.parseditems = []

    def append_item(self, parseditem):
        self.parseditems.append(parseditem)

    def set_introduction_paragraph(self, paragraph):
        self.introduction_paragraph = paragraph

    def to_dict(self):
        dict = {}
        dict['heading'] = self.heading
        if self.introduction_paragraph == None:
            dict['intro'] = ''
        else:
            dict['intro'] = repr(self.introduction_paragraph.rawtext)

        return dict


class AbstractParsedQuestionChildItem(AbstractParsedItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        pass
