from csc import divisi2
from csc.divisi2.blending import blend
from csc.util.persist import PickleDict
from verb_reader import verb_reader

pd = PickleDict('./pickledir/')

def make_exclude_file(game):
    overlist = []
    gamematix = divisi2.load(game + '.pickle')
    nouns = gamematix.row_labels
    overlist += nouns
    overlist += verb_reader(game+'.inf')
    overlist = [x.lower() for x in overlist]
    return overlist
    
def getWNSim(word1, word2):
    from nltk.corpus import wordnet as wn
    syn1 = wn.synsets(word1)
    syn2 = wn.synsets(word2)
    high = 0
    for syna in syn1:
        for synb in syn2:
            cur = 0
            try:
                cur =  syn1.wup_similarity(syn2)
            except:
                cur =  -4000
            if cur > high: high = cur
    return high
    
def NotOverRide(game, object):
    if game in pd and 'over' in pd[game]:
        overlist = pd[game]['over']
    else:
        overlist = make_exclude_file(game)
        pd[game]['over'] = overlist
    if object in overlist: return False
    return True

def top_non_game_sims(game, object, n=6):
    if game in pd:
        similarity = pd[game]['blend']
    else:
        similarity = make_blend(game + '.pickle')
    frame = divisi2.SparseVector.from_counts([object])
    sim = similarity.right_category(frame)
    all = sim.top_items(n*2)
    return [x for x in all if NotOverRide(game, x[0])]
#    clear = [(getWNSim(object, x[0]), x) for x in all if NotOverRide(game, x)]
#    clear.sort()
#    return [x[1] for x in clear][:n]

def game_sims(game, object, n=6, threshold=1):
    if game in pd:
        similarity = pd[game]['blend']
    else:
        similarity = make_blend(game + '.pickle')
    frame = divisi2.SparseVector.from_counts([object])
    sim = similarity.right_category(frame)
    all = sim.top_items(n*2)
    return [x for x in all if not NotOverRide(game, x[0]) or x[1] >= threshold]
#    clear = [(getWNSim(object, x[0]), x) for x in all if NotOverRide(game, x)]
#    clear.sort()
#    return [x[1] for x in clear][:n]


def make_blend(thefile):
    conceptnet = divisi2.network.conceptnet_matrix('en').normalize_all()
    thegame = divisi2.load(thefile).normalize_all()
    blended_matrix = blend([conceptnet, thegame], [0.9, 0.1])
    u,s,v = blended_matrix.svd()
    
    similarity = divisi2.reconstruct_similarity(u, s) # offset=1.5) 
    pd.mkdir(thefile.split('.')[0])
    pd[thefile.split('.')[0]]['blend'] = similarity
    return similarity

def understand(game, object):
    #top_stuff = top_non_game_sims(game, object)
    top_stuff = game_sims(game, object)
    print game, object, top_stuff
    #if top_stuff[0][1] == 0.0:
    #    print "Object not found: ", object
    #    return ""
    #return 'Understand "' + '" or "'.join([x[0] for x in top_stuff]) + '" as the ' + object + '.'

def game_synonyms(game, threshold=1):
    dict = {}
    for obj in divisi2.load(game + '.pickle').row_labels:
        dict[obj] = [ x[0] for x in game_sims(game, obj, threshold=threshold) ]
    return dict

def synonyms(game, topics, threshold=1):
    conv_syms = game_synonyms(game, threshold)
    for topic in topics:
        if topic in conv_syms.keys(): continue
        else:
            conv_syms[topic] = [x[0] for x in game_sims(game, topic, threshold=threshold)]
    return conv_syms

#print understand('story', 'recommend')

#understand('bronze', 'hut')
#understand('bronze', 'house')
#understand('bronze', 'taste')
#understand('bronze', 'cow')
#understand('bronze', 'castle')
#understand('bronze', 'old woman')

#synonyms('davissquare', 0)
