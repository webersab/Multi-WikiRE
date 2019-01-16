import sys
import json
import new_newsqa_evaluator as Evaluator


def load_dict(fname):
    with open(fname, 'r') as fp:
        data = json.load(fp)
    return data


#dataset = .prepend_nil
#orig. = .configd
dataset = load_dict('')
orig_dataset = load_dict('')

pred = load_dict(sys.argv[1])
for key in pred.keys():
    if 'NIL' in pred[key]:
        pred[key] = "NIL"

#gold = dataset['data']
#gold = load_dict(dataset)
#for key in gold.keys():
#    if 'NIL' in pred[key]:
#        pred[key] = "NIL"



#print "=" * 50
#print(Evaluator.evaluate(orig_dataset['data'], pred))
#print "On non-nil data (w/o NIL)"

#print "=" * 50

corr_nil = 0.0
pred_nil = 0.0
total_nil = 0

"""
for key in pred.keys():
    print("key: ", key)
    if 'NONE' in key:
        total_nil += 1
        if 'NIL' in pred[key]:
            corr_nil += 1.0
    if 'NIL' in pred[key]:
        pred_nil += 1.0
"""

"""
for value, g in zip(pred.values(), gold) :
    print("val: ", value, "g: ", g)
    if  'NIl' in g:
        total_nil += 1
        if 'NIL' in value:
            corr_nil += 1.0
    if 'NIL' in value:
        pred_nil += 1.0

nil_p = corr_nil / pred_nil
nil_r = corr_nil / total_nil
print "NIL prec:", corr_nil / pred_nil
print "NIL recl:", corr_nil / total_nil
print "NIL F1:", 2 * nil_p * nil_r / (nil_p + nil_r)
print "=" * 50
"""
print "Overall scores:"
print(Evaluator.evaluate(dataset['data'], pred))
print "Overall scores:"
print "=" * 50

