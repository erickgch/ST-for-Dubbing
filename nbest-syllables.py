# improvements with respect to nbest-take1: for each source segment, if no hypothesis with the same number of 
    # syllables is found within the first 25, take the best ranked hypothesis with the closes number of syllables. 

import sys
import re
import pylabeador
import pyphen
from nltk.corpus import cmudict


infile = '/media/erickgch/EGC/MT-FBK-internship/nbest/test.test.es.sys' 
outfile_eng = infile + 'src_.txt'
outfile_spa = infile + 'trg_.txt'
n = 50
bests = [] #contains selected hypotheses
orig = [] # contains translations

# syllables and nUM_syl are functions that allow counting syllables in ENGLISH. For Spanish, pylabeador is used.

def syllables(word):
    #referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

d = cmudict.dict()

def num_syl(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except KeyError:
        #if word not found in cmudict
        return syllables(word)

with open(infile) as inf, open(outfile_spa, 'w') as out_trg, open(outfile_eng,'w') as out_src:
    for line in inf:
        if line.startswith('|') or line[0] == 'N' or line[0] == 'P':
            # skip irrelevant lines
            continue
        elif line.startswith('S-'):
            # human translation
            s_syl_count = 0
            temp_ = []
            source = line.strip().split('\t')[1].strip('.,?!')
            #counting source syllables
            for w in source.split():
                temp_.append(num_syl(w))
            s_syl_count = sum(temp_)
            
            ref = next(inf)
            translation = line.strip().split('\t')
            #bests.append(source)
            first_ = '' # < --- in case the top ranked hypothesis is needed
            current_best = 20
            temp_ = '' # <--- buffer storing the best result. If no hypothesis with a smaller number of syls is found, this will be moved to bests
            for i in range(n):
            # loop over the hypotheses
                h_syl_count = 0
                hyp = next(inf)
                prob = next(inf)
                hypothesis = hyp.strip().split('\t')[2] # get only the text
                if i == 1:
                    first_ = hypothesis
                # counting target syllables
                selected = ' '.join(re.findall('\w+', hypothesis)).split()
                hyp_sylls = []
                for w in selected:
                    try:
                        sylls = pylabeador.syllabify(w)
                    except:
                        sylls = [w]
                    hyp_sylls = hyp_sylls + sylls
                h_syl_count = len(hyp_sylls)
                if abs(h_syl_count - s_syl_count) < current_best:
                    current_best = abs(h_syl_count- s_syl_count)
                    temp_ = hypothesis
                
            bests.append(temp_)

