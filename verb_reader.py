def verb_reader(filename):
    file = open(filename)
    verbs = set()
    for line in file:
        line = line.strip()
        if line.startswith('Verb'):
            parts = line.split()
            for part in parts[1:]:
                verbs.add(part.strip("'/"))
    return verbs

print verb_reader('bronze_compiled.inf')
