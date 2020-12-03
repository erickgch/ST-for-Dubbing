# Commas, semicolons and periods are considered to be pauses. 

import sys
import re

infile = '/media/erickgch/EGC/MT-FBK-internship/nbest/test.test.es.sys' 
outfile_eng = infile + 'src_.txt'
outfile_spa = infile + 'trg_.txt'
n = 50
bests = []


with open(infile) as inf, open(outfile_spa, 'w') as out_trg, open(outfile_eng,'w') as out_src:
    for line in inf:
        if line.startswith('|') or line[0] == 'N' or line[0] == 'P':
            # skip irrelevant lines
            continue
        elif line.startswith('S-'):
            # human translation
            s_pau_count = 0
            temp_ = []
            source = line.strip().split('\t')[1].strip('.,?!')
            #bests.append('***'+source+'***')
            #counting source pauses
            pauses_ = re.findall('(,|\.|;)\B', source)
            s_pau_count = len(pauses_)

            ref = next(inf)
            translation = line.strip().split('\t')
            first_ = ''
            for i in range(n):
            # loop over the hypotheses
                h_pau_count = 0
                hyp = next(inf)
                prob = next(inf)
                hypothesis = hyp.strip().split('\t')[2] # get only the text
                if i == 1:
                    first_ = hypothesis
                # counting target syllables
                pauses_h = re.findall('(,|\.|;)\B', hypothesis)
                h_pau_count = len(pauses_h)
                if h_pau_count == s_pau_count:
                    bests.append(hypothesis)
                    break
                elif i > 25:
                    # get first hypothesis if none with the same number of syllables if found within the first 25
                    bests.append(first_)
                    break
   
            
with open('nbest-pauses.txt', 'w') as f:
    for item in bests:
        f.write("%s\n" % item)
