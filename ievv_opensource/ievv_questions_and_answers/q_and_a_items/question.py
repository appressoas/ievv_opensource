import re

from ievv_opensource.ievv_questions_and_answers.q_and_a_items.abstract_item import AbstractParsedItemWithChildren
from ievv_opensource.ievv_questions_and_answers import parse_exceptions


class Question(AbstractParsedItemWithChildren):

    @classmethod
    def match(cls, rawtext):
        return re.match(r'^::.*$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Question, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.typeid = None

    def append_item(self, parseditem):
        if self.parseditems:
            if self.typeid != parseditem.get_typeid():
                raise parse_exceptions.QuestionTypeIdParseError(
                    linenumber=parseditem.linenumber,
                    errormessage='Can not mix types within a question'
                )
        else:
            self.typeid = parseditem.get_typeid()
        super(Question, self).append_item(parseditem)

    def to_dict(self):
        dict = super(Question, self).to_dict()
        dict['options'] = []

        return dict