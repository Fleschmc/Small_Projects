import pandas as pd
import itertools

def cloning(clist, numr = 4, gen = 'False', depth = 3):
    genes = {'w' : 0.9, 'x' : 0.9,  'g' : 0.5, 'h' : 0.5, 'y' : 0.5}
    zero =  {'w' : 0,   'x' : 0,    'g' : 0,   'h' : 0,   'y' : 0}
    score = {'w' : -0.5,  'x' : -0.5, 'g' : 1,   'h' : 0.5, 'y' : 1}
    master = []
    
    def do_stuff():
        for _ in range(9):
            combs = list(itertools.combinations_with_replacement(clist, _))
            for comb in combs:
                clones = list(comb).copy()
                item = [list(zip([genes[gene] for gene in list(clone)], list(clone))) for clone in clones]
                inter = []
                for num in range(6):
                    thing = zero.copy()
                    for i in item:
                        thing[i[num][1]] += i[num][0]
                    inter.append(thing)
                put = [max(_, key = _.get) for _ in inter]
                data_dict = {}
                data_dict['product'] = ''.join(put)
                data_dict['score']   = sum([score[p] for p in put])
                data_dict['clones']  = clones
                data_dict['num_clones'] = len(clones)
                if any([''.join(put) == x for x in clist]) == True:
                    data_dict['n/o'] = 'old'
                else:
                    data_dict['n/o'] = 'new'
                master.append(data_dict)
        return pd.DataFrame(master).sort_values(['score', 'n/o', 'num_clones'], ascending = (False, True, True))[['product', 'score', 'n/o', 'clones']].drop_duplicates(subset=['product'], keep = 'first')
    
    df = do_stuff()
    if gen == 'True':
        aclist = df[df['n/o'] == 'new']['product'].tolist()
        if len(aclist) >= depth:
            aclist = aclist[:depth]
            clist = clist + aclist
        else:
            clist = clist + aclist
        df = do_stuff()
        return df[:numr], aclist 
           
    else:
        return df[:numr]