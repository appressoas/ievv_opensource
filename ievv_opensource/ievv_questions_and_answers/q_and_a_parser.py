from ievv_opensource.ievv_questions_and_answers.q_and_a_items.paragraph import Paragraph
from ievv_opensource.ievv_questions_and_answers.q_and_a_items.question import Question
from ievv_opensource.ievv_questions_and_answers.q_and_a_items.section import Section

from ievv_opensource.ievv_questions_and_answers.q_and_a_items import option_types

from ievv_opensource.ievv_questions_and_answers import parse_exceptions

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


class Parse(object):
    @classmethod
    def from_rawtext(cls, rawtext):
        parser = cls()
        parser.parse(rawtext=rawtext)
        return parser

    def __init__(self):
        self.sections = []
        self.current_section = None
        self.current_question = None
        self.parsers = []
        self.parsers.extend(self.get_sectioning_parsers())
        self.parsers.extend(self.get_question_child_parsers())

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
            option_types.SingleSelectOption,
            option_types.MultiSelectOption,
            option_types.Textarea,
            option_types.Range,
        ]

    def parse_line(self, line):
        for lineparser in self.parsers:
            if lineparser.match(line):
                return lineparser, line
        return 'paragraphline', line

    def parse(self, rawtext):
        consumed_paragraph_lines = []
        consumed_paragraph_first_linenumber = None
        for linenumber, line in enumerate(rawtext.split('\n'), 1):
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
        # print('heading', repr(line))
        section = lineparser(rawtext=line, linenumber=linenumber)
        self.current_section = section
        self.sections.append(section)

    def parse_question_start(self, lineparser, line, linenumber):
        # print('question', repr(line))
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
                raise parse_exceptions.ParagraphParseError(
                    linenumber=linenumber,
                    errormessage='Misplaced paragraph: {!r}'.format(lines)
                )
            # print('paragraph', repr(paragraphtext))
            paragraph = Paragraph(rawtext=paragraphtext, linenumber=linenumber)
            if paragraphtype == 'sectionintro':
                self.current_section.set_introduction_paragraph(paragraph)
            else:
                self.current_question.set_introduction_paragraph(paragraph)
        else:
            pass
            # print('EMPTY paragraph')


if __name__ == '__main__':
    parser = Parse.from_rawtext(source)
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