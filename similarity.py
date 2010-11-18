from csc import divisi2
def make_sim():
    # Get similarity from the expanded version of ConceptNet.
    # This is not blended with anything yet.
    conceptnet = divisi2.load('conceptnet_big.pickle')
    U, S, V = conceptnet.svd(k=100)
    sim = divisi2.reconstruct_similarity(U, S, offset=0.1)
    return sim


