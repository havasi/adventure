from pyparsing import *
from collections import defaultdict

def join_words(lst):
    return ' '.join(lst)

currentID = ""
idsToNames = defaultdict(list)

# keywords
K_WITH = Literal("with")
K_HAS = Literal("has")
K_CLASS = Literal("class")

# top-level definition keywords
D_OBJECT = Literal("Object")
D_CLASS = Literal("Class")

# keywords that follow "with"
W_NAME = Literal("name")
W_SHORT_NAME = Literal("short_name")
W_DESCRIPTION = Literal("description")
W_FOUND_IN = Literal("found_in")
W_PLURAL = Literal("plural")

# punctuation
TILDE = Literal("~").suppress()
ARROW = Literal("->")
SEMICOLON = Literal(";").suppress()

new_identifier = Word(alphanums+'_')
identifier = Word(alphanums+'_')
name_list = Group(OneOrMore(sglQuotedString.setParseAction(lambda p: p[0].strip("'"))))
num_arrows = ZeroOrMore(ARROW).setParseAction(len)
quoted_name = dblQuotedString.setParseAction(lambda p: p[0].strip('"'))

def name_lister(parse):
    if currentID:
        for name in parse[2]:
            idsToNames[currentID].append(name)
        return []

def name_assigner(parse):
    if currentID:
        idsToNames[currentID].append(parse[2])
    return []

def id_assigner(parse):
    global currentID
    currentID = parse[-1]
    return []

def id_forgetter(parse):
    global currentID
    currentID = None

has_line = K_HAS + identifier
has_line.setParseAction(lambda p: [('HasProperty', p[1], True)])
hasnt_line = K_HAS + TILDE + identifier
hasnt_line.setParseAction(lambda p: [('HasProperty', p[1], False)])
name_line = K_WITH + W_NAME + name_list
name_line.setParseAction(name_lister)
shortname_line = K_WITH + W_SHORT_NAME + quoted_name
plural_line = K_WITH + W_PLURAL + quoted_name
canonical_name_line = (shortname_line | plural_line).setParseAction(name_assigner)

found_in_line = K_WITH + W_FOUND_IN + identifier
found_in_line.setParseAction(lambda p: [('AtLocation', p[2], True)])
class_line = K_CLASS + identifier
class_line.setParseAction(lambda p: [('IsA', p[1], True)])

object_def = D_OBJECT + num_arrows + new_identifier + dblQuotedString.suppress()
class_def = D_CLASS + new_identifier

defn_line = ((object_def | class_def) + stringEnd).setParseAction(id_assigner)
prop_line = (has_line | hasnt_line | name_line | canonical_name_line
             | found_in_line | class_line) + stringEnd
defn_end = (SEMICOLON + stringEnd).setParseAction(id_forgetter)
inform_line = (defn_line | prop_line | defn_end)

def inform_parser(file):
    assertions = []
    for line in file:
        try:
            parse_out = inform_line.parseString(line.strip())
            if currentID is not None:
                new_features = [(currentID,) + feature for feature in parse_out]
                if new_features:
                    print new_features
                assertions.extend(new_features)
        except ParseException:
            continue

    named_assertions = []
    for assertion in assertions:
        id, rel, target, polarity = assertion
        names = idsToNames[id]
        for name in names:
            if target in idsToNames:
                targetnames = idsToNames[target]
            else:
                targetnames = [target]
            for targetname in targetnames:
                named = (name, rel, targetname, polarity)
                print named
                named_assertions.append(named)
    return named_assertions
inform_parser(open('bronze_compiled.inf'))

