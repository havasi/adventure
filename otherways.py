from csc import divisi2
from csc.divisi2.blending import blend
from csc.util.persist import PickleDict
from nltk.corpus import wordnet as wn

pd = PickleDict('./pickledir/')

def getWNSim(word1, word2):
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
        file = open(game + '.over', 'r')
        overlist = file.readlines()
        file.close()
        overlist = [x.lower().replace('\n', '') for x in overlist]
    if object in overlist: return False
    return True

def top_game_sims(game, object, n=6):
    if game in pd:
        similarity = pd[game]['blend']
    else:
        similarity = make_blend(game + '.pickle')
    frame = divisi2.SparseVector.from_counts([object])
    sim = similarity.right_category(frame)
    all = sim.top_items(n*2)
    clear = [(getWNSim(object, x[0]), x) for x in all if NotOverRide(game, x)]
    clear.sort()
    return [x[1] for x in clear][:n]
    

def make_blend(thefile):
    conceptnet = divisi2.network.conceptnet_matrix('en').normalize_all()
    thegame = divisi2.load(thefile).normalize_all()
    blended_matrix = blend([conceptnet, thegame])
    u,s,v = blended_matrix.svd()
    
    similarity = divisi2.reconstruct_similarity(u, s) #, post_normalize=False)
    pd.mkdir(thefile.split('.')[0])
    pd[thefile.split('.')[0]]['blend'] = similarity
    return similarity

def understand(game, object):
    top_stuff = top_game_sims(game, object)
    return 'Understand "' + '" or "'.join([x[0] for x in top_stuff]) + '" as the ' + object + '.'

print understand('bronze', 'hut')
print understand('bronze', 'house')
print understand('bronze', 'taste')
print understand('bronze', 'cow')
print understand('bronze', 'castle')
print understand('bronze', 'old women')
