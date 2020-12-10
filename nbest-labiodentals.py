# obtain the highest ranking hypothesis with the closes number of word-initial bilabials to the source 

import sys
import re
import pylabeador
import pyphen
from nltk.corpus import cmudict


infile = '/media/erickgch/EGC/MT-FBK-internship/nbest/test.test.es.sys' 
outfile_eng = infile + 'src_.txt'
outfile_spa = infile + 'trg_.txt'
n = 50
bests = []
orig = []

# syllables and nUM_syl are functions that allow counting syllables in ENGLISH. For Spanish, pylabeador is used.

with open(infile) as inf, open(outfile_spa, 'w') as out_trg, open(outfile_eng,'w') as out_src:
    for line in inf:
        if line.startswith('|') or line[0] == 'N' or line[0] == 'P':
            # skip irrelevant lines
            continue
        elif line.startswith('S-'):
            # human translation
            s_phon_count = 0
            temp_ = []
            source = line.strip().split('\t')[1].strip('.,?!')
            #bests.append('***'+source+'***')
            #counting source syllables
            for w in source.split():
                phon_match = ' '.join(re.findall('^(f|v)', w.lower())).strip() # substitute (f|v) for (p|m|b) if looking at bilabials
                if len(phon_match) > 0:
                    temp_.append(phon_match)
            s_phon_count += len(temp_)
            
            ref = next(inf)
            translation = line.strip().split('\t')
            first_ = ''
            current_best = 20 
            temp_ = '' # <--- buffer storing the current best hypothesis
            for i in range(n):
            # loop over the hypotheses
                h_phon_count = 0
                hyp = next(inf)
                prob = next(inf)
                hypothesis = hyp.strip().split('\t')[2] # get only the text
                hyp_temp_ = []
                if i == 1:
                    first_ = hypothesis
                # counting target syllables
                for w in hypothesis.split():
                    phon_match = ' '.join(re.findall('^(f|v)', w.lower())).strip() # substitute (f|v) for (p|m|b) if looking at bilabials
                    if len(phon_match) > 0:
                        hyp_temp_.append(phon_match)
                h_phon_count += len(hyp_temp_)
                
                if abs(h_phon_count - s_phon_count) < current_best:
                    current_best = abs(h_phon_count - s_phon_count)
                    temp_ = hypothesis
                    
            bests.append(temp_)
