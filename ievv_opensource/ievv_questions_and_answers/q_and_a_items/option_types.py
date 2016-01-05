import re

from ievv_opensource.ievv_questions_and_answers.q_and_a_items.abstract_item import AbstractParsedQuestionChildItem


class SingleSelectOption(AbstractParsedQuestionChildItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        return re.match(r'^\((-?\d+)\)(.*)$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(SingleSelectOption, self).__init__(rawtext=rawtext, linenumber=linenumber)
        match = self.__class__.match(rawtext)
        self.number = match.group(1)
        self.text = match.group(2).strip()

    def get_typeid(self):
        return 'singleselect'

    def to_dict(self):
        dict = {}
        dict['type'] = self.get_typeid()
        dict['points'] = int(self.number)
        dict['is_checked'] = False
        dict['text'] = self.text

        return dict

    def __str__(self):
        return '[{}]: {!r}'.format(self.number, self.text)


class MultiSelectOption(AbstractParsedQuestionChildItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\[(-?\d+)\](.*)$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(MultiSelectOption, self).__init__(rawtext=rawtext, linenumber=linenumber)
        match = self.__class__.match(rawtext)
        self.number = match.group(1)
        self.text = match.group(2).strip()

    def get_typeid(self):
        return 'multiselect'

    def to_dict(self):
        dict = {}
        dict['type'] = self.get_typeid()
        dict['points'] = self.number
        dict['is_checked'] = False
        dict['text'] = self.text

        return dict

    def __str__(self):
        return '({}): {!r}'.format(self.number, self.text)


class Range(AbstractParsedQuestionChildItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\{(\d+)-(\d+)\}$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Range, self).__init__(rawtext=rawtext, linenumber=linenumber)
        match = self.__class__.match(rawtext)
        self.from_number = match.group(1)
        self.to_number = match.group(2)

    def get_typeid(self):
        return 'range'

    def to_dict(self):
        dict = {}
        dict['type'] = self.get_typeid()
        dict['from_number'] = int(self.from_number)
        dict['to_number'] = int(self.to_number)

        return dict

    def __str__(self):
        return '{{{}-{}}}'.format(self.from_number, self.to_number)


class Textarea(AbstractParsedQuestionChildItem):
    """

    """
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\[(.*?)\]$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Textarea, self).__init__(rawtext=rawtext, linenumber=linenumber)
        match = self.__class__.match(rawtext)
        self.text = match.group(1)

    def get_typeid(self):
        return 'textarea'

    def to_dict(self):
        dict = {}
        dict['type'] = self.get_typeid()
        dict['text'] = self.text

        return dict