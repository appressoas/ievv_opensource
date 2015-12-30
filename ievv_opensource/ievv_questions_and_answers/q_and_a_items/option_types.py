import re

from ievv_opensource.ievv_questions_and_answers.q_and_a_items.abstract_item import AbstractParsedQuestionChildItem


class SingleSelectOption(AbstractParsedQuestionChildItem):
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

    def __str__(self):
        return '[{}]: {!r}'.format(self.number, self.text)


class MultiSelectOption(AbstractParsedQuestionChildItem):
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

    def __str__(self):
        return '({}): {!r}'.format(self.number, self.text)


class Range(AbstractParsedQuestionChildItem):
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

    def __str__(self):
        return '{{{}-{}}}'.format(self.from_number, self.to_number)


class Textarea(AbstractParsedQuestionChildItem):
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\[\.\.\.\]$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Textarea, self).__init__(rawtext=rawtext, linenumber=linenumber)

    def get_typeid(self):
        return 'textarea'