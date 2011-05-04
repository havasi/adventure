from pyparsing import *
from collections import defaultdict
from csc import divisi2
from csc.nl import get_nl
from locations import Inform6Parser
from verb_reader import verb_reader

english = get_nl('en')

def parseText(thingy):
    _, ident, string = thingy
    concepts = english.extract_concepts(string, max_words=2, check_conceptnet=True)
    for concept in concepts:
        # CAH - This is quite possibly highly sketch.  If this doesn't work, we'll have to spectral.
        descriptions[ident].append(('HasProperty', concept, True))
    return []
    
def join_words(lst):
    return ' '.join(lst)

currentID = ""
idsToNames = defaultdict(list)
descriptions = defaultdict(list)

# keywords
K_WITH = Literal("with")
K_HAS = Literal("has")
K_CLASS = Literal("class")

# top-level definition keywords
D_OBJECT = Literal("Object")
D_CLASS = Literal("Class")
D_CONSTANT = Literal("Constant")

# keywords that follow "with"
W_NAME = Literal("name")
W_SHORT_NAME = Literal("short_name")
W_DESCRIPTION = Literal("description")
W_FOUND_IN = Literal("found_in")
W_PLURAL = Literal("plural")

# punctuation
TILDE = Literal("~").suppress()
EQUALS = Literal("=").suppress()
ARROW = Literal("->")
SEMICOLON = Literal(";").suppress()

new_identifier = Word(alphanums+'_')
identifier = Word(alphanums+'_')
name_list = Group(OneOrMore(sglQuotedString.setParseAction(lambda p: p[0].strip("'"))))
num_arrows = ZeroOrMore(ARROW).setParseAction(lambda p: len(p))
quoted_name = dblQuotedString.setParseAction(lambda p: p[0].strip('"'))

def name_lister(parse):
    if currentID:
        for name in parse[2]:
            idsToNames[currentID].append(name)
        return []

def name_assigner(parse):
    if currentID:
        idsToNames[currentID].append(parse[2].replace('^',"'"))
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
desc_line = K_WITH + W_DESCRIPTION + identifier
desc_line.setParseAction(lambda p: [('__description', p[2], True)])

class_line = K_CLASS + identifier
class_line.setParseAction(lambda p: [('IsA', p[1], True)])

object_def = D_OBJECT + num_arrows + new_identifier + dblQuotedString.suppress()
class_def = D_CLASS + new_identifier
constant_def = D_CONSTANT + new_identifier + EQUALS + (sglQuotedString | dblQuotedString)
constant_def.setParseAction(parseText)

defn_line = ((object_def | class_def | constant_def) + stringEnd).setParseAction(id_assigner)
prop_line = (has_line | hasnt_line | name_line | canonical_name_line
            | desc_line | found_in_line | class_line) + stringEnd
defn_end = (SEMICOLON + stringEnd).setParseAction(id_forgetter)
inform_line = (defn_line | prop_line | defn_end)

def inform_parser(filename):
    assertions = []
    file = open(filename)
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
    file.close()
    
    new_assertions = []
    for assertion in assertions:
        if assertion[1] == '__description':
            for feature in descriptions[assertion[2]]:
                new_assertions.append((assertion[0],) + feature)
        else:
            new_assertions.append(assertion)
    assertions = new_assertions

    print assertions
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

    locations = Inform6Parser(filename).parents
    for key, values in locations.items():
        for value in values:
            for name1 in idsToNames[key]:
                for name2 in idsToNames[value]:
                    named = (name1, 'AtLocation', name2, True)
                    print named
                    named_assertions.append(named)

    return named_assertions

def make_divisi_matrix(filename):
    parsedlist = inform_parser(filename)
    game = filename.split('.')[0]
    thinglist = [(1 if x[3] else -1, english.normalize(x[0].replace('^', "'")), ('right', x[1], english.normalize(x[2].replace('^', "'")))) for x in parsedlist]
    # Write out the confusingly-named overlist. First, the nouns.
    overlist = open(game + '.over', 'w')
    for concept1, rel, concept2, val in parsedlist:
        if rel == 'HasProperty' and concept2 == 'mark_as_thing':
            print >> overlist, concept1
            print concept1

    # Now the verbs.
    verbs = verb_reader(filename)
    for verb in verbs:
        print >> overlist, verb
    overlist.close()

    game_matrix = divisi2.make_sparse(thinglist).normalize_all()
    divisi2.save(game_matrix, game + '.pickle')
    return game_matrix
    
if __name__ == '__main__':
    import sys
    matrix = make_divisi_matrix(dict(enumerate(sys.argv)).get(1, 'glass.inf'))
