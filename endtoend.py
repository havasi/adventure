from convertInform import pullAllTopics
from convertInform import convertFile
#convertFile, pullAllTopics
from otherways import synonyms
import divisi2
from simplenlp import get_nl

en_nl = get_nl('en')


# Davis Square
#topics = pullAllTopics('DavisSquare.txt')
#para = synonyms('davissquare', topics, 0)
#convertFile(para, 'DavisSquare.txt', 'AIwashere.txt')

topics = pullAllTopics('Glass.txt')
topics = [en_nl.normalize(x) for x in topics]
para = synonyms('glass', topics, 0)
convertFile(para, 'Glass.txt', 'new_glass.txt')
assert False

# Glass - rough
'''
conceptnet = divisi2.network.conceptnet_matrix('en').normalize_all()
u,s,v = conceptnet.svd()
similarity = divisi2.reconstruct_similarity(u, s) # offset=1.5)

def make_sim_rough(object, topics, n=2):
    frame = divisi2.SparseVector.from_counts([object])
    sim = similarity.right_category(frame)
    all = sim.top_items(n*2)
    return [x for x in all if x[0] not in topics]


topics = pullAllTopics('Glass.txt')
for object in topics:
    print object
    print make_sim_rough(object, topics)'''

