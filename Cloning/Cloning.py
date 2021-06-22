import pandas as pd
import numpy as np
import itertools
from collections import Counter

class Cloning():
    genes = {'w' : 0.9,  'x' : 0.9,  'g' : 0.5, 'h' : 0.5, 'y' : 0.5} # How Rust weights genes when calculating dominance
    zero =  {'w' : 0,    'x' : 0,    'g' : 0,   'h' : 0,   'y' : 0}   # Used for calculating dominance
    score = {'w' : -0.5, 'x' : -0.25, 'g' : 1,   'h' : 0.5, 'y' : 1}   # My scoring dictionary
    
    def __init__(self, clist, ncross_breed, gen, depth):
        self.clist = clist
        self.ncross_breed = ncross_breed
        self.gen = gen
        self.depth = depth
        self.master = []

    def create_combs(self, clist, ncross_breed, gclist):
        combs  = [itertools.combinations_with_replacement(clist, _) for _ in range(1, ncross_breed + 1)]
        combs  = [item for sublist in combs for item in sublist]
        if gclist:
            combs = set([tuple(_) for _ in pd.DataFrame(self.master)['clones']]) ^ set(combs)  # Removing all the clones already calculatd
        return combs
    
    def check_comb(self, comb):
        if any([value > (0.5 * len(comb)) for value in list(Counter(comb).values())]): # Checks if more than half the clones are the same
            return False 
        else:
            return True
    
    def calculate_score(self, comb):
        clones = list(comb).copy()
        clones_weighted = [list(zip([Cloning.genes[gene] for gene in list(clone)], list(clone))) for clone in clones]
        inter = []
        for num in range(6): # six because there are six genes per clone
            zero_copy = Cloning.zero.copy()
            for i in clones_weighted:
                zero_copy[i[num][1]] += i[num][0] # Calculating which gene is dominant for each gene slot
            inter.append(zero_copy)

        put, problems, solutions = [max(_, key = _.get) for _ in inter], [], [] 
        for i, x in enumerate(inter):
            duptest, ip = [value == max(x.values()) for value in list(x.values())], [] # duptest tests each gene column for a 50/50 shot
            if sum(duptest) > 1:
                for j, y in enumerate(duptest):
                    if y == True:
                        ip.append((i, list(x.keys())[j]))
            if len(ip) > 0:
                problems.append(ip)

        if len(problems) > 0:    
            for x in list(itertools.product(*problems)):
                for y in x:
                    tput = put.copy()
                    del tput[y[0]]
                    tput.insert(y[0], y[1])
                    solutions.append(tput)
            solutions, im = [tuple(_) for _ in solutions], [] # im: Intermediate Master
            for product in set(solutions):            
                data_dict = {}
                data_dict['product']    = ''.join(product)
                data_dict['score']      = sum([Cloning.score[p] for p in product])
                data_dict['clones']     = clones
                data_dict['num_clones'] = len(clones)
                im.append(data_dict)
            return im
        else:
            data_dict = {}
            data_dict['product']    = ''.join(put)
            data_dict['score']      = sum([Cloning.score[p] for p in put])
            data_dict['clones']     = clones
            data_dict['num_clones'] = len(clones)
            return [data_dict] # must be a list to concatenate to master

    def generate(self, depth = 5):
        go, clist, aclist, gclist, removed = True, self.clist, [], [], []
        while go:
            combs = self.create_combs(clist, self.ncross_breed, gclist)
            for comb in combs:
                if self.check_comb(comb):
                    self.master += self.calculate_score(comb)

            df = pd.DataFrame(self.master)
            df['n/o'] = np.where(df['product'].isin(clist), 'old', 'new')
            df = df.sort_values(['score', 'n/o', 'num_clones'], ascending = (False, True, True))[['product', 'score', 'n/o', 'clones']].drop_duplicates(subset=['product'], keep = 'first')

            if self.gen:
                aclist = df[(df['n/o'] == 'new') & (df['score'] >= max(df['score']) - 3 / max(df['score']))]

                if gclist:
                    # Ensures we aren't adding in clones that have already been removed and also giving clones a 1 generation grace period before being removed
                    aclist = aclist[(-aclist['product'].isin(removed)) & (-aclist['product'].isin([_[0] for _ in gclist[-1]]))]

                if len(aclist):
                    if len(aclist) > depth:
                        gclist.append(list(zip(aclist['product'][:depth], aclist['clones'][:depth], aclist['score'][:depth])))
                        clist = clist + aclist['product'].tolist()[:depth]
                    else:
                        gclist.append(list(zip(aclist['product'], aclist['clones'], aclist['score'])))
                        clist = clist + aclist['product'].tolist()
                
                    if gclist:
                        cdict = {}
                        for c in clist:
                            cdict[c] = 0
                            for m in aclist['clones']:
                                if c in m:
                                    cdict[c] += 1
                            if cdict[c] < 0.05 * len(aclist): # removing clones that aren't in at least 5% of the new clones
                                clist.remove(c)
                                removed.append(c)
                else:
                    return df[:4], gclist # implement numr and replace 4 with numr

            else:
                go = False
        return df[:4] 
            
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
    dest  = 'clist',
    nargs = '+',
    help  = 'This is the list of clones you want to crossbreed. Type them with one space apart e.g. hhhhhh yyyyyy gggggg'
    )
    
    parser.add_argument(
    dest = 'ncross_breed',
    type = int,
    help = 'This is the maximum number of clones you want to cross breed with. Bigger numbers will increase run time. Typically 4-6 works well.'
    )
    
    parser.add_argument(
    '-g', '--generate',
    dest = 'gen',
    action ='store_true',
    help = 'Indicates that the function should act generatively. Crossbreed, add best clones, repeat until no new good clones.'
    )

    parser.add_argument(
    '-d', '--depth',
    dest = 'depth',
    type = int,
    help = 'This is the number of new clones to be added with each generation. Only supply a value if using --generate. Default = 5. Syntax: -d 5 or --depth 5'
    )

    args = vars(parser.parse_args())

    cloner = Cloning(**args)

    print(cloner.generate())