import re

from ievv_opensource.ievv_questions_and_answers.q_and_a_items.abstract_item import AbstractParsedItemWithChildren


class Section(AbstractParsedItemWithChildren):
    """

    """
    @classmethod
    def match(cls, rawtext):
        return re.match(r'^##.*$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Section, self).__init__(rawtext=rawtext, linenumber=linenumber)

    def to_dict(self):
        dict = super(Section, self).to_dict()
        dict['questions'] = []

        return dict
