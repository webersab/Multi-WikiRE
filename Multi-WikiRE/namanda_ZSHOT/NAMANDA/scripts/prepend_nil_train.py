import json
import sys


def load_dict(fname):
    with open(fname, 'r') as fp:
        data = json.load(fp)
    return data


fname = sys.argv[1]
data = load_dict(fname)
for i,a in enumerate(data['data']):
    a['paragraphs'] = [p[0] for p in  a['paragraphs']]
    for p in a['paragraphs']:
        #p = p[0]
        #print(p)
        p['context'] = 'NIL ' + p['context']
        for qa in p['qas']:
            #for ans in qa['answers']:
            #print(qa, qa['answer'])
            ans = qa['answer'][0]
            if ans['text'] == 'NIL' or ans['answer_start'] == -1:
                ans['answer_start'] = 0
                ans['text'] = 'NIL'
            else:
                ans['answer_start'] = int(ans['answer_start']) + 4
        #print(p)
            #for ans in qa['all_answers']:
            #    if ans['text'] == 'NIL' or ans['answer_start'] == -1:
            #        ans['answer_start'] = 0
                #else:
                #    ans['answer_start'] = int(ans['answer_start']) + 4

with open(fname + '.prepend_nil', 'w') as fp:
    json.dump(data, fp)
