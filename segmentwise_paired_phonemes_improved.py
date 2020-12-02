# phoneme alignment
from os.path import join
import textgrids
from os import listdir
import collections
import pandas as pd

path = '/media/erickgch/EGC/MT-FBK-internship/alignments/all'
en_path = join(path + '_eng')
es_path = join(path + '_spa')
all_en = ['n', '@U', 'D', 'I', 's', 'z', 'w', '3`', 'E', 'R', '<p:>', 't',
               'eI', 'k', 'v', 'i:', 'V', 'aI', 'u', 'f', 'd', 'N', 'Q', 'l', 'm',
               '{', 'b', '6', 'p', 'u:', 'g', '4', 'h', 'aU', 'T', 'j', 'dZ', '?',
               'h\\', 'O:', 'm=', '@', 'U', 'tS', 'S', 'l=', 'OI', 'Z', 'I@', 'n=', 'r']
all_es = ['<p:>', 'i', 'k', 'j', 'e', 'r', 'm', 'B', 'N', 'g', 'a', 'n', 'T', 'l', 'o', 'p', 'd', 't', 'D', 'z', 's',
          'w', 'G', 'u', 'f', 'F', 'x', 'tS', 'rr', 'L', 'jj', 'J', 'b', 'S']

'''
def word_initial(infile):
    firsts, phonemes = [], []
    try:
        grid = textgrids.TextGrid(infile)
        idx = 1
        for word in grid['KAN-MAU']:
            if word != '':
                firsts.append(word.xmax)
        if grid['MAU'][0].text == '<p:>':
            displace = float(grid['MAU'][0].xmax)
        else:
            displace = 0
        for it in grid['MAU']:
            if it.xmax in firsts:
                phonemes.append([it.text, (it.xmin - displace, it.xmax - displace)])
    except TypeError:
        print('File ' + infile + ' not in proper TextGrid format')
    return phonemes
'''


def save_grid(infile):
    # Read a textgrid and return a list of a list of the phoneme and its timings
    phonemes = []
    try:
        grid = textgrids.TextGrid(infile)
        if grid['MAU'][0].text == '<p:>':
            displace = float(grid['MAU'][0].xmax)
        else:
            displace = 0
        for it in grid['MAU']:
            phonemes.append([it.text, (it.xmin - displace, it.xmax - displace)])
    except TypeError:
        print('File ' + infile + ' not in proper TextGrid format')

    return phonemes


def overlapps(phons_en, phons_es):
    # Given two lists of en and es phonemes, find time-overlapping phonemes
    overlaps = []
    for ph in phons_es:
        phoneme = ph[0]
        start = float(ph[1][0])
        end = float(ph[1][1])
        for p in phons_en:
            phoneme_en = p[0]
            start_en = float(p[1][0])
            end_en = float(p[1][1])
            if start_en <= start < end_en:
                overlaps.append((phoneme_en, phoneme))
                # print(ph, p) # all overlaps
            if start_en < end <= end_en:
                overlaps.append((phoneme_en, phoneme))
    return overlaps


def count_overs(phon_overl):
    count_list = []
    for i in phon_overl:
        tot = Counter(i)
        count_list.append(tot)
    return count_list


overs = []
files = listdir(en_path)
for f in files:
    temp_ = []
    en = join(en_path, f)
    try:
        es = join(es_path, f.replace('_eng', '_spa'))
        #phons_en = word_initial(en)
        #phons_es = word_initial(es)
        phons_en = save_grid(en)
        phons_es = save_grid(es)
        ovlps = overlapps(phons_en, phons_es)
        if ovlps:
            temp_ += ovlps
    except FileNotFoundError:
        print('File not found: ' + es)
    overs.append(temp_)

    
phoneme_classes = {'pause':['<p:>'],'bilabial':['p','b','B','m','m='],'dentolabial':['f','v'],
                   'dental':['d','D','t','T','dZ','s','z','S','tS','rr','r','4','n','l','l=','jj','L','R'],
                   'velar':['g','G','k','N'],'back post vowel':['O:','OI','U','u:', 'Q', 'V','w','@U','o','u'],
                   'closed vowel':['i','I','I@','i:','j'],'mid vowel':['e','3`','E','@','@`','eI'],'open vowel':['6','{','a']}
def get_matches(overlap_data):
    match_phons = []
    for seg in overlap_data:
        temp_ = []
        matches_list = []
        for k,v in phoneme_classes.items():
            p_c_temp = {}
            #m_count = match count, p_count = all instances of given phoneme in EN
            m_count, p_count = 0, 0
            for i in seg:
                if i[0] in v:
                    p_count += 1
                    if i[1] in v:
                        m_count +=1
                        matches_list.append(i)
                    else:
                        pass
                else:
                    pass
            p_c_temp = {k:(m_count,p_count)}
            temp_.append(p_c_temp)
            super_d = {}
            pmatches_d = {'matches':matches_list}
            #put all phon category counts in a single dict
        for d in temp_:
            for k, v in d.items():
                super_d.setdefault(k,v)
                temp_ = [super_d, pmatches_d]
        match_phons.append(temp_)

    #create dict with total percentage of matches per segment and dict with segment id
    for f,seg in zip(files,match_phons):
        count_a, count_b = 0, 0
        for k,v in seg[0].items():
            count_a += v[0]
            count_b += v[1]
        try:        
            seg.append({'total':(count_a/count_b)})
            seg.append({'seg_id':str(f)})
        except ZeroDivisionError:
            seg.append({'total':0})
            seg.append({'seg_id':str(f)})
    
    return match_phons

def find_high_segs(matches):
#Get id of segments where (phoneme) matches surpass 50%
    hits = []
    for seg in matches:
        id_ = seg[-1].get('seg_id')
        for d in seg:
            for k,v in d.items():
                if k == 'total' and v >= 0.5:
                    hits.append(id_)
    return hits

my_matches = get_matches(overs)

for seg in my_matches:
    print(seg[1], seg[3])
