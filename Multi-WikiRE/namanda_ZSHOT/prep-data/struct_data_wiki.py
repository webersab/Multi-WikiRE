from collections import defaultdict
import json
import sys
from joblib import Parallel, delayed
import itertools


"""
def config_data(data):
    #
    ctxs = [p['context'] for p in data['data'][0]['paragraphs']]
    qas = [p['qas'][0] for p in data['data'][0]['paragraphs']]
    # qas = sum(qas, [])
    ctx_set = set(ctxs)
    ctx_list = list(ctx_set)
    new_data = {}
    new_data['version'] = data['version']
    # new_data['data'] = []
    # new_data['paragraphs'] = []
    paras = []
    for ctx in ctx_list:
        paradict = {}
        paradict['context'] = ctx
        paradict['qas'] = []
        for i in range(len(ctxs)):
            if ctxs[i] == ctx:
                paradict['qas'].append(qas[i])
        paras.append(paradict)
    new_data['data'] = [{'paragraphs': paras}]
    # new_data['paragraphs'] = paras
    return new_data
"""

def config_data(data):
    """
    ctxs = [p['context'] for p in data]
    q = [p['question'] for p in data]
    a = [p['answer'] for p in data]
    start_index = [p['start_index'] for p in data]
    end_index = [p['end_index'] for p in data]
    """
    ctxs = []
    q = []
    a = []
    start_index = []
    end_index = []
    ids = []
    for p in data:
        p = json.loads(p)
        ctxs.append(p['context']) 
        q.append(p['question']) 
        a.append(p['answer']) 
        start_index.append(p['start_index'])
        end_index.append(p['end_index']) 
        ids.append(p['id'])
    ctx_set = set(ctxs)
    ctx_list = list(ctx_set)
    new_data = {}

    new_data['version'] = "v0.1"

    #new_data['data'] = []
    #new_data['paragraphs'] = []
      
    paras = []
    id_tracker = []
    for ctx in ctx_list:
        paradict = {}
        paradict['context'] = ctx
        paradict['qas'] = []
        #[{"qas": [{"answer": [{"text": "U.S. President-elect Barack Obama ", "answer_start": "63"}], "question": "Iran criticizes who?", 
        #"id": "0", "answers": [{"text": "President-elect Barack Obama ", "answer_start": "68"}, {"text": "U.S. President-elect Barack Obama ", #"answer_start": "63"}], 
        #"validated_answers": "{\"63:97\": 2}"}]
        for i in range(len(ctxs)):
            if ctxs[i] == ctx and ids[i] not in  id_tracker:
                #build qas
                id_tracker.append(ids[i])
                qas = {"answer": [ {"text": a[i], "answer_start": start_index[i]} ], "question": q[i], "id": ids[i], "answers": [], "validated_answers": ""}
                paradict['qas'].append(qas)
        paras.append(paradict)
    new_data['data'] = [{'paragraphs': paras}]

    # new_data['paragraphs'] = paras
    return new_data


def config_data_fixed(data):
    ctxs = []
    q = []
    a = []
    start_index = []
    end_index = []
    paras = []
    new_data = {}
    new_data['version'] = "v0.1"
    paras = defaultdict(list)

    for i, p in enumerate(data):
        p = json.loads(p)
        #ctxs.append(p['context'])
#       if  p['context'] not in paras.keys():
        if  p['context'] not in paras:
            paradict = {}
            paradict['context'] = p['context']
            paradict['qas'] = []
            qas = {"answer": [ {"text": p['answer'], "answer_start": p['start_index']} ], "question": p['question'], "id": i, "answers": [], "validated_answers": ""}
            paradict['qas'].append(qas)
            paras[p['context']].append(paradict)
        else:
            qas = {"answer": [ {"text": p['answer'], "answer_start": p['start_index']} ], "question": p['question'], "id": i, "answers": [], "validated_answers": ""}
            #print( paras[p['context']])
            paras[p['context']][0]['qas'].append(qas)     
            #print("after:", paras[p['context']])

        #q.append(p['question'])
        #a.append(p['answer'])
        #start_index.append(p['start_index'])
        #end_index.append(p['end_index'])
    paras = paras.values()
    new_data['data'] = [{'paragraphs': paras}]

    ctx_set = set(ctxs)
    ctx_list = list(ctx_set)
    print(len(ctx_list), len(ctxs), len(paras))
    return new_data


    """
    new_data = {}
    new_data['version'] = "v0.1"
    paras = []
    for ctx in ctx_list:
        paradict = {}
        paradict['context'] = ctx
        paradict['qas'] = []
        for i in range(len(ctxs)):
            if ctxs[i] == ctx:
                #build qas
                qas = {"answer": [ {"text": a[i], "answer_start": start_index[i]} ], "question": q[i], "id": i, "answers": [], "validated_answers": ""}
                paradict['qas'].append(qas)
        paras.append(paradict)
    new_data['data'] = [{'paragraphs': paras}]
    """
    # new_data['paragraphs'] = paras

def config_data_par(data):

    #new_data['data'] = []
    #new_data['paragraphs'] = []
    print(data[0])    
    all = Parallel(n_jobs=32, verbose=1, backend="threading")(
             map(delayed(par_buidldlists), data))   
    #print(all)
    ctxs, q, a, start_index, end_index = [a[0][0] for a in all], [a[1][0] for a in all], [a[2][0] for a in all], [a[3][0] for a in all], [a[4][0] for a in all] 
    paras = []
    ctx_set = set(ctxs)
    ctx_list = list(ctx_set)
    new_data = {}
    new_data['version'] = "v0.1"
    """
    for ctx in ctx_list:
        paradict = {}
        paradict['context'] = ctx
        paradict['qas'] = []
        for i in range(len(ctxs)):
            if ctxs[i] == ctx:
                #build qas
                qas = {"answer": [ {"text": a[i], "answer_start": start_index[i]} ], "question": q[i], "id": i, "answers": [], "validated_answers": ""}
                paradict['qas'].append(qas)
        paras.append(paradict)
    """
    #results = Parallel(n_jobs=num_cores)(delayed(processInput)(i,j) for i,j in zip(a,b))
    paras = Parallel(n_jobs=32, verbose=1, backend="threading")(delayed(par_paras) (ctxs_list_item, ctxs_it, q_it, a_it, start_index_it, end_index_it) for ctxs_list_item, ctxs_it, q_it, a_it, start_index_it, end_index_it in zip_with_scalar(ctx_list, ctxs, q, a, start_index, end_index))
    print(paras)
    new_data['data'] = [{'paragraphs': paras}]

    # new_data['paragraphs'] = paras
    return new_data

def zip_with_scalar(l, a,b,c,d,e ):
    return zip(l, itertools.repeat(a), itertools.repeat(b), itertools.repeat(c),itertools.repeat(d), itertools.repeat(e))

def par_buidldlists(p):
     ctxs = []
     q = []
     a = []
     start_index = []
     end_index = []
     #for p in data:
     p = json.loads(p)
     ctxs.append(p['context'])
     q.append(p['question'])
     a.append(p['answer'])
     start_index.append(p['start_index'])
     end_index.append(p['end_index'])
     return ctxs, q, a, start_index, end_index

def par_paras(ctxs_list_item,ctxs, q, a, start_index, end_index):
     paradict = {}
     paradict['context'] = ctxs_list_item
     paradict['qas'] = []
     for i in range(len(ctxs)):
            if ctxs[i] == ctxs_list_item:
                #build qas
                qas = {"answer": [ {"text": a[i], "answer_start": start_index[i]} ], "question": q[i], "id": i, "answers": [], "validated_answers": ""}
                paradict['qas'].append(qas)
     #paras.append(paradict)
     return paradict

"""
def load_dict(fname):
    with open(fname, 'r') as fp:
        data = json.load(fp)
    return data
"""

def load_dict(fname):
    #with open(fname, 'r') as fp:
    #    full_data = json.load(fp)
    with open(fname, 'r') as fp:
        data = fp.readlines()
    return data




fname = ''
fnamedev = ''
fnametest = ''






if True:
    data = load_dict(fname)

#new_dataa = config_data(data)
new_dataa = config_data_fixed(data)
if True: 
    with open(fname + '.configd', 'w') as fp:
        json.dump(new_dataa, fp)

    data = load_dict(fnamedev)
    new_dataa = config_data(data)
    with open(fnamedev + '.configd', 'w') as fp:
        json.dump(new_dataa, fp)

    data = load_dict(fnametest)
    new_dataa = config_data(data)
    with open(fnametest + '.configd', 'w') as fp:
        json.dump(new_dataa, fp)
