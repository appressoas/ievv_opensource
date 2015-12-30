class ParseError(Exception):
    def __init__(self, linenumber, errormessage):
        self.linenumber = linenumber
        self.errormessage = errormessage
        super(ParseError, self).__init__(u'{}: {}'.format(linenumber, errormessage))


class ParagraphParseError(ParseError):
    pass


class QuestionTypeIdParseError(ParseError):
    pass