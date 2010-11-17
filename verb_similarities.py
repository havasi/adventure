import pickle
from csc.nl import get_nl
from csc import divisi2

en_nl = get_nl('en')
A = divisi2.network.conceptnet_matrix('en')
A_pre = A.normalize_all()
U_pre, S_pre, V_pre = A_pre.svd(k=100)
sim_pre = divisi2.reconstruct_similarity(U_pre, S_pre, post_normalize=False)
def output_verb_similarities(filename):
    verbs = []
    f = open(filename)
    understands = pickle.load(f)
    f.close()

    
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
        #TODO: detect verbs + stopwords, for instance "putting it on"

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
                print new_verb
        except KeyError:
            pass
        print '\n' 
            
output_verb_similarities('bronze_output.pickle')
