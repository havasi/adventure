from convertInform import pullAllTopics
#convertFile, pullAllTopics
from otherways import synonyms
import divisi2

# Davis Square
#topics = pullAllTopics('DavisSquare.txt')
#para = synonyms('davissquare', topics, 0)
#convertFile(para, 'DavisSquare.txt', 'AIwashere.txt')

conceptnet = divisi2.network.conceptnet_matrix('en').normalize_all()
u,s,v = conceptnet.svd()
similarity = divisi2.reconstruct_similarity(u, s) # offset=1.5)

# Glass
def make_sim_rough(object, topics, n=2):
    frame = divisi2.SparseVector.from_counts([object])
    sim = similarity.right_category(frame)
    all = sim.top_items(n*2)
    return [x for x in all if x[0] not in topics]


topics = pullAllTopics('Glass.txt')
for object in topics:
    print object
    print make_sim_rough(object, topics)

