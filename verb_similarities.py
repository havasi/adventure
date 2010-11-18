import pickle
from csc.nl import get_nl
from csc import divisi2
from similarity import make_sim

en_nl = get_nl('en')
"""
A = divisi2.network.conceptnet_matrix('en')
A_pre = A.normalize_all()
U_pre, S_pre, V_pre = A_pre.svd(k=100)
sim_pre = divisi2.reconstruct_similarity(U_pre, S_pre, post_normalize=False)
"""

sim_pre = make_sim()

def output_verb_similarities(filename):
    verbs = []
    f = open(filename)
    understands = pickle.load(f)
    f.close()

    
    #verbs that have meaning in game.  Shouldn't give them other meanings.  
    dont_overload =set(['ignite', 'restore', 'all', 'adjust', 'help', 'burn', 'show', 'dance', 'skip', 'random', 'actions', 'bring', 'kill', 'rooms', 'shake', 'go', 'polish', 'yes', 'find', 'silence', 'blow', 'bang', 'squeeze', 'untie', 'pray', 'menu', 'except', 'eat', 'about', 'shout', 'version', 'descend', 'present', 'crack', 'carve', 'sorry', 'save', 'retreat', 'kick', 'take', 'swim', 'then', 'move', 'hit', 'torture', 'get', 'rules', 'hint', 'watch', 'rush', 'strut', 'break', 'answer', 'unwrap', 'every', 'darn', 'kiss', 'tie', 'press', 'awaken', 'wipe', 'restart', 'look', 'insert', 'rotate', 'exits', 'wash', 'inventory', 'drop', 'stroll', 'l', 'remove', 'leave', 'p', 'stuff', 'each', 'x', 'grab', 'steal', 'dir', 'view', 'sew', 'shed', 'set', 'knock', 'unscrew', 'pronouns', 'showme', 'prune', 'touch', 'see', 'meta', 'holler', 'run', 'wander', 'creep', 'out', 'snuff', 'scale', 'yodel', 'wreck', 'deactivate', 'jump', 'normal', 'brief', 'melt', 'everything', 'hear', 'score', 'exit', 'superbrief', 'hiss', 'drink', 'dirs', 'shut', 'full', 'showverb', 'quit', 'rub', 'thump', 'inspect', 'deliver', 'punch', 'undo', 'credits', 'consult', 'cut', 'wear', 'uncover', 'put', 'sing', 'directions', 'throw', 'wait', 'shine', 'both', 'search', 'incinerate', 'sniff', 'shove', 'roar', 'of', 'script', 'o', 'display', 'chop', 'stride', 'objects', 'place', 'stand', 'pick', 'discard', 'climb', 'think', 'gonear', 'feed', 'info', 'depart', 'verbose', 'curses', 'feel', 'wave', 'embroider', 'sweep', 'wrap', 'walk', 'whisper', 'ask', 'activate', 'long', 'another', 'carry', 'resuscitate', 'ring', 'open', 'speak', 'showheap', 'use', 'proceed', 'injure', 'free', 'scry', 'bite', 'smash', 'revive', 'relations', 'fight', 'purloin', 'attach', 'attack', 'damn', 'tell', 'lock', 'strike', 'scope', 'hug', 'inv', 'board', 'breathe', 'murder', 'complete', 'offer', 'hum', 'acquire', 'squash', 'but', 'snatch', 'shroud', 'observe', 'wake', 'stick', 'hurl', 'hold', 'cleanse', 'disrobe', 'fullscore', 'hints', 'me', 'pull', 'myself', 'sleep', 'g', 'places', 'things', 'bother', 'tree', 'scenes', 'n', 'unlock', 'shift', 'kindle', 'extinguish', 'z', 'fetch', 'say', 'and', 'listen', 'loosen', 'tap', 'give', 'taste', 'toss', 'abstract', 'describe', 'fuck', 'ransack', 'twist', 'examine', 'buy', 'embrace', 'rap', 'close', 'return', 'turn', 'seek', 'check', 'shit', 'fill', 'again', 'sip', 'end', 'no', 'pay', 'self', 'fling', 'novice', 'cross', 'verify', 'revisit', 'read', 'nap', 'other', 'amusing', 'hop', 'notify', 'test', 'destroy', 'unlockall', 'smell', 'start', 'ascend', 'drat', 'play', 'finish', 'scrub', 'trace', 'screw', 'back', 'stop', 'dive', 'swing', 'reach', 'sneak', 'hand', 'push', 'drag', 'slice', 'nouns', 'fasten', 'dust', 'glklist', 'transcript', 'swallow', 'muffle', 'stitch', 'purchase', 'short', 'don', 'remember', 'whistle', 'i', 'light', 'clear', 'sit', 'cover', 'smack', 'greet', 'doff', 'q', 'switch', 'solve', 'oops', 'clean', 'enter', 'y', 'awake', 'yell', 'scream', 'squint'])
 
    
    for item in understands:
        add = False
        poss_verb = item[1]
        if poss_verb.endswith('ing'):
            add = True
        words = poss_verb.split()
        if words[0].endswith('ing'):
            add = True
            for word in words[1:]:
                if en_nl.is_stopword(word) == False:
                    add = False
                    break
        
        if add:
            verbs.append(item)
            

    for item in verbs:
        #assume that items that end in 'ing' are a verb.  NOTE: Could cause 
        #some misidentifications, "ring" comes to mind.

        print item
        #to extract the content of the verb phrase, need to split it at first stopword
        #or anything that starts with a bracket
        verb = ""
        for word in item[0].split(' '):
             if en_nl.is_stopword(word):
                 break
             if word.startswith('['):
                 break
             if word.find('/') != -1:
                 break
             verb = verb + word + ' ' 
        verb = verb[:-1]
        rest = item[0][len(verb):]
        print verb
        try:
            sims = sim_pre.row_named(verb)
            for similar_item in sims.top_items():
                new_verb = [similar_item[0] + ' ' + rest, item[1]]
                if similar_item[0] not in dont_overload:
                  print new_verb
        except KeyError:
            pass
        print '\n' 
            
output_verb_similarities('bronze_output.pickle')
