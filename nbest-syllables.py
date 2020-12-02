import sys
import re
import pylabeador
from nltk.corpus import cmudict


infile = '/media/erickgch/EGC/MT-FBK-internship/nbest/test.test.es.sys' 
outfile_eng = infile + 'src_.txt'
outfile_spa = infile + 'trg_.txt'
n = 50
bests = []

# syllables and num_syl are functions that allow counting syllables in ENGLISH. For SPANISH, pylabeador is used.

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
            bests.append('***'+source+'***')
            #counting source syllables
            for w in source.split():
                temp_.append(num_syl(w))
            s_syl_count = sum(temp_)
            
            ref = next(inf)
            translation = line.strip().split('\t')
            for i in range(n):
            # loop over the hypotheses
                h_syl_count = 0
                hyp = next(inf)
                prob = next(inf)
                hypothesis = hyp.strip().split('\t')[2] # get only the text
                
                # counting target syllables
                selected = ' '.join(re.findall('\w+', hypothesis)).split()
                hyp_sylls = []
                for i in selected:
                    try:
                        sylls = pylabeador.syllabify(i)
                    except:
                        sylls = [i]
                    hyp_sylls = hyp_sylls + sylls
                h_syl_count = len(hyp_sylls)
                if h_syl_count == s_syl_count:
                    bests.append(hypothesis)
                    break


with open('nbest-syllables', 'w') as f:
    for item in bests:
        f.write("%s\n" % item)


