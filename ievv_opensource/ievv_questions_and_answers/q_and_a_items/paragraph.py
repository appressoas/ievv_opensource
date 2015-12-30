from ievv_opensource.ievv_questions_and_answers.q_and_a_items.abstract_item import AbstractParsedItem

class Paragraph(AbstractParsedItem):
    @classmethod
    def match(cls, rawtext):
        pass

    def __init__(self, rawtext, linenumber):
        super(Paragraph, self).__init__(rawtext=rawtext, linenumber=linenumber)

    def __str__(self):
        return repr(self.rawtext)