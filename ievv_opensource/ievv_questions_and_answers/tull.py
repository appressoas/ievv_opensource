import re

source = """## A section heading

Donec id elit non mi porta gravida at eget metus. Maecenas faucibus mollis interdum.
Vestibulum id ligula porta felis euismod semper. Sed posuere consectetur est at lobortis.
Donec id elit non mi porta gravida at eget metus. Nullam quis risus eget urna mollis ornare vel eu leo.

Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Cum sociis natoque penatibus
et magnis dis parturient montes, nascetur ridiculus mus. Maecenas faucibus mollis interdum.
Nullam quis risus eget urna mollis ornare vel eu leo. Vestibulum id ligula porta felis euismod semper.
Maecenas faucibus mollis interdum. Lorem ipsum dolor sit amet, consectetur adipiscing elit.

:: How well did the student solve feature X?
(-5) Rally badly.
(5) A usable solution, but not a good solution.
(15) A fairly decent solution.
(30) A more or less perfect solution.

:: Please rate the solution:
0 means awful and 100 means perfect.
{0-100}

:: Type in some extra feedback
[...]

## Section 2

:: The earth is
Select the correct answers (if any)
[1] Round
[1] Larger than the moon
[-3] Flat
[-2] 6000 years old
"""


class ParseError(Exception):
    def __init__(self, linenumber, errormessage):
        self.linenumber = linenumber
        self.errormessage = errormessage
        super(ParseError, self).__init__(u'{}: {}'.format(linenumber, errormessage))


class ParagraphParseError(ParseError):
    pass


class QuestionTypeIdParseError(ParseError):
    pass


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
    def __init__(self, rawtext, linenumber):
        super(AbstractParsedItemWithChildren, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.introduction_paragraph = None
        self.parseditems = []

    def append_item(self, parseditem):
        self.parseditems.append(parseditem)

    def set_introduction_paragraph(self, paragraph):
        self.introduction_paragraph = paragraph


class AbstractParsedQuestionChildItem(AbstractParsedItem):
    def get_typeid(self):
        raise NotImplementedError()


class Section(AbstractParsedItemWithChildren):

    @classmethod
    def match(cls, rawtext):
        return re.match(r'^##.*$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Section, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.heading = rawtext[2:].strip()


class Question(AbstractParsedItemWithChildren):

    @classmethod
    def match(cls, rawtext):
        return re.match(r'^::.*$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Question, self).__init__(rawtext=rawtext, linenumber=linenumber)
        self.heading = rawtext[2:].strip()
        self.typeid = None

    def append_item(self, parseditem):
        if self.parseditems:
            if self.typeid != parseditem.get_typeid():
                raise QuestionTypeIdParseError(
                    linenumber=parseditem.linenumber,
                    errormessage='Can not mix types within a question'
                )
        else:
            self.typeid = parseditem.get_typeid()
        super(Question, self).append_item(parseditem)


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


class Textarea(AbstractParsedQuestionChildItem):
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\[\.\.\.\].*$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Textarea, self).__init__(rawtext=rawtext, linenumber=linenumber)

    def get_typeid(self):
        return 'textarea'


class Range(AbstractParsedQuestionChildItem):
    @classmethod
    def match(cls, rawtext):
        return re.match(r'\{(\d+)-(\d+)\}(.*)$', rawtext)

    def __init__(self, rawtext, linenumber):
        super(Range, self).__init__(rawtext=rawtext, linenumber=linenumber)
        match = self.__class__.match(rawtext)
        self.from_number = match.group(1)
        self.to_number = match.group(2)
        self.text = match.group(3).strip()

    def get_typeid(self):
        return 'range'

    def __str__(self):
        return '{{{}-{}}}: {!r}'.format(self.from_number, self.to_number, self.text)


class Paragraph(AbstractParsedItem):
    def __init__(self, rawtext, linenumber):
        super(Paragraph, self).__init__(rawtext=rawtext, linenumber=linenumber)

    def __str__(self):
        return repr(self.rawtext)


class Parse(object):

    def get_section_parser_class(self):
        return Section

    def get_question_parser_class(self):
        return Question

    def get_sectioning_parsers(self):
        return [
            self.get_section_parser_class(),
            self.get_question_parser_class(),
        ]

    def get_question_child_parsers(self):
        return [
            SingleSelectOption,
            MultiSelectOption,
            Textarea,
            Range,
        ]

    def __init__(self, source):
        self.source = source
        self.sections = []
        self.current_section = None
        self.current_question = None
        self.parsers = []
        self.parsers.extend(self.get_sectioning_parsers())
        self.parsers.extend(self.get_question_child_parsers())
        self.parse()

    def parse_line(self, line):
        for lineparser in self.parsers:
            if lineparser.match(line):
                return lineparser, line
        return 'paragraphline', line

    def parse(self):
        consumed_paragraph_lines = []
        consumed_paragraph_first_linenumber = None
        for linenumber, line in enumerate(source.split('\n'), 1):
            lineparser, line = self.parse_line(line.strip())
            if lineparser == 'paragraphline':
                consumed_paragraph_lines.append(line)
                if consumed_paragraph_first_linenumber is None:
                    consumed_paragraph_first_linenumber = linenumber
            else:
                if consumed_paragraph_lines:
                    self.parse_paragraph(consumed_paragraph_lines,
                                         linenumber=consumed_paragraph_first_linenumber)
                    consumed_paragraph_lines = []
                    consumed_paragraph_first_linenumber = None
                self.handle_parsable_line(lineparser=lineparser, line=line, linenumber=linenumber)
        if consumed_paragraph_lines:
            self.parse_paragraph(consumed_paragraph_lines,
                                 linenumber=consumed_paragraph_first_linenumber)

    def handle_parsable_line(self, lineparser, line, linenumber):
        if issubclass(lineparser, Section):
            self.parse_section_start(lineparser=lineparser, line=line, linenumber=linenumber)
        elif issubclass(lineparser, Question):
            self.parse_question_start(lineparser=lineparser, line=line, linenumber=linenumber)
        else:
            self.current_question.append_item(lineparser(rawtext=line, linenumber=linenumber))

    def parse_section_start(self, lineparser, line, linenumber):
        print('heading', repr(line))
        section = lineparser(rawtext=line, linenumber=linenumber)
        self.current_section = section
        self.sections.append(section)

    def parse_question_start(self, lineparser, line, linenumber):
        print('question', repr(line))
        question = lineparser(rawtext=line, linenumber=linenumber)
        self.current_question = question
        self.current_section.append_item(question)

    def get_paragraph_type(self, linenumber):
        if self.current_section or self.current_question:
            if self.current_section.linenumber == linenumber - 1:
                return 'sectionintro'
            elif self.current_question.linenumber == linenumber - 1:
                return 'questionintro'
        else:
            return None

    def parse_paragraph(self, lines, linenumber):
        paragraphtext = '\n'.join(lines).strip()
        if paragraphtext:
            paragraphtype = self.get_paragraph_type(linenumber=linenumber)
            if paragraphtype is None:
                raise ParagraphParseError(
                    linenumber=linenumber,
                    errormessage='Misplaced paragraph: {!r}'.format(lines)
                )
            print('paragraph', repr(paragraphtext))
            paragraph = Paragraph(rawtext=paragraphtext, linenumber=linenumber)
            if paragraphtype == 'sectionintro':
                self.current_section.set_introduction_paragraph(paragraph)
            else:
                self.current_question.set_introduction_paragraph(paragraph)
        else:
            print('EMPTY paragraph')


if __name__ == '__main__':
    parser = Parse(source)
    for section in parser.sections:
        print()
        print("*" * 70)
        print(section.heading)
        print("*" * 70)
        print(section.introduction_paragraph)
        for question in section.parseditems:
            print()
            print()
            print('QUESTION: {}'.format(question.heading))
            print('intro: {}'.format(question.introduction_paragraph))
            for item in question.parseditems:
                print('{}: {}'.format(item.get_typeid(), item))
