def verb_reader(filename):
    file = open(filename)
    verbs = set()
    for line in file:
        line = line.strip()
        if line.startswith('Verb'):
            parts = line.split()
            for part in parts[1:]:
                verbs.add(part.strip("'/"))
        if line.startswith('Constant'):
            parts = line.split()
            if parts[1].endswith('__WD') or parts[1].endswith('__KY'):
                keyword = parts[-1]
                assert keyword.startswith("'")
                assert keyword.endswith("';")
                verbs.add(keyword[1:-2].lower().strip('/'))
    return verbs

verbs = verb_reader('bronze_compiled.inf')
print verbs
