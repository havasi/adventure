from pyparsing import *

def join_words(p):
    return ' '.join(p[0])

UNDERSTAND = Literal("understand")
AS = Literal("as").suppress()
QUOTE = Literal('"').suppress()
PERIOD = Literal('.').suppress()
nameword = Word(alphas+"'-")
name = Group(OneOrMore(nameword))
article = Optional(Literal("a ") | Literal("an ") | Literal("the ")).suppress()
np = (article + name).setParseAction(join_words)
termlist = Group(delimitedList(dblQuotedString, "or"))
dblQuotedString.setParseAction(removeQuotes)

understand_instruction = UNDERSTAND + termlist + AS + np + stringEnd

def understand_verb_reader(file):
    got = []
    for sentence in file.read().split('.'):
        try:
            parsed = understand_instruction.parseString(sentence.lower())
            keyword, sources, target = parsed
            for source in sources:
                got.append([source, target])
                print [source, target]
        except ParseException:
            pass
    return got

print understand_verb_reader(open('bronze.ni'))
