# source
# https://github.com/duyet/vietnamese-namedb
# https://github.com/thuy-le-ep/Vietnamese-data/tree/master/Vietnamese%20person%20names

import ahocorasick 
import itertools
import pickle
import json
import ast
import re

from utils.util import save

def read(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            line = re.sub(' +', ' ',line)
            data.append(line.replace('\n', '').lower())
    return data

def build_full_name(
    fn_path = './first_name.txt',
    mn_path = './mid_name.txt',
    ln_path = './last_name.txt'
    ):
    # fn = read(fn_path)
    # mn = read(mn_path)
    # ln = read(ln_path)

    # mid + last name
    # ml = itertools.product(mn, ln)
    # ml = [' '.join(item) for item in ml]
    
    # first + mid + last name
    # fml =  itertools.product(fn, ml)
    # fml = [' '.join(item) for item in fml]
    # print("Saving first + mid + last name ...")
    # save(fml,'fullname2.txt')

    # first + first name
    # ff = itertools.product(fn, fn)
    # ff = [' '.join(item) for item in ff]

    # first + first + mid + last name
    ml = read('./midlastname.txt')
    ff = read('./firstfirstname.txt')
    ffml =  itertools.product(ff, ml)
    ffml = [' '.join(item) for item in ffml]

    # Save to txt 
    # ffml.extend(fml)
    # ffml = list(set(ffml))
    print("Saving first + first + mid + last name ...")
    save(ffml,'fullname2.txt')
def build_dict(
    path='./fullname.txt',
    path_out = './data/fullname.pkl'
    ):

    full_name = read(path)

    fullname_dict = ahocorasick.Automaton()

    idx = 0
    for key in full_name:
        fullname_dict.add_word(key, (idx, key))
        idx += 1

    fullname_dict.make_automaton()

    print('Saving dictionary ...')
    with open(path_out, 'wb') as file:
        pickle.dump(fullname_dict, file)
        

if __name__ == '__main__':
    # build_full_name()

    build_dict(
        path='./stopwords.txt',
        path_out = './data/stopwords.pkl'
    )