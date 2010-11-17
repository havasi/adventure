#!/usr/bin/python
import re
import sys
import collections

class Inform6Parser:
    def __init__(self, name):
        self.parents = collections.defaultdict(set)
        self.names = {}
        self.filename = name
        self._parse()
    
    def _parse(self):
        path = {}
        for line in open(self.filename):
            words = line.strip().split()
            if len(words) < 2:
                continue
            if words[0] == 'Object':
                i = 1
                while words[i] == '->':
                    i += 1
                path[i] = current = words[i]
                if i > 1:
                    self.parents[current].add(path[i-1])
            elif words[:2] == [ 'with', 'found_in' ]:
                self.parents[current].update(words[2:])
            elif words[:2] == [ 'with', 'short_name' ]:
                self.names[line.strip().split(None, 2)[2].strip('"' + "'")] = current

if __name__ == '__main__':
    '''
    This does break on I283_stinky, which has
        with found_in [; if (TestRegionalContainment(location, I282_stinky)) rtrue; ],
    but I think 'with found_in' is only for environmental objects so it should be fine.
    '''
    for k, v in Inform6Parser('bronze_compiled.inf').parents.items():
        print '%-28s' % k, list(v)
