# This script looks at the frequency of synchronic phoneme-to-phoneme matches for any pair of aligned segments. (e.g. /p/ in ENG --> /p/ in SPA)

import pandas as pd

path_ = input()

def handle_df(path):
    df = pd.read_csv(path,  delimiter='\t', index_col='Phonemes')
    #clean df
    df.loc['h'] = df.loc['h'] + df.loc['h\\']
    df = df.drop(columns=['Unnamed: 0'],index=['r', 'h\\']).rename(index={'R':'r'})
    
    return df

#phonemes
#eng_phones = ['<p:>', 'aI', 'l', 'g', 'E', 't', 'D', 'V', 'b', '{', 'k', 'n', 'j', 'u', '@U', 'v', 'R', 'i:', 'T', 'I', 'N', 'aU', '?', 'd', 'S', 'z', 'h', 'dZ', 's', 'u:', '3`', 'f', 'O:', 'U', 'h\\', 'p', 'm', 'Q', 'w', 'eI', '4', 'n=', 'OI', '6', 'tS', '@', 'l=', 'I@', 'Z', 'r', 'm=']
#spa_phones = ['s', 'i', '<p:>', 'u', 'l', 't', 'm', 'a', 'e', 'n', 'p', 'j', 'o', 'tS', 'B', 'D', 'k', 'x', 'f', 'r', 'jj', 'G', 'w', 'T', 'd', 'S', 'L', 'z', 'rr', 'g', 'b', 'N', 'J', 'F']

on_aligned_freqs, off_aligned_freqs, mix_aligned_freqs = [], [], []

# tuple structure: (english allophones, spanish allophones)
common_allophones = [(['<p:>'], ['<p:>']),(['d'], ['d','D']), (['D'],['d', 'D']), (['n','N','n='], ['n','N']), 
                     (['S'],['S']), (['T'],['T']), (['b'],['b', 'B']), (['f'],['f']), (['g'],['g', 'G']), 
                     (['j'],['j']), (['k'], ['k']), (['l'], ['l']), (['m', 'm='], ['m']), (['p'], ['p']), 
                     (['r'],['r']), (['s'], ['s','z']), (['z'], ['s','z']), (['t'],['t']), (['tS'],['tS']),
                     (['u', 'U', 'u:'],['u']), (['w'],['w']), (['E', '3`', '@'], ['e']), (['{', '6'], ['a'])]

def get_freqs(df):
    #phoneme frequencies in English
    
    aligned_freqs = []
    
    for a in common_allophones:
        for i in a[0]:
            temp = []
            for k in a[1]:
                x = (i, df.loc[i][k])
                temp.append(x[1])
            tempsum = sum(temp)
            aligned_freqs.append((x[0], tempsum))
    
    product_l = []
    
    for phon in aligned_freqs:
        try:
            row_ = int(df.loc[phon[0]].sum())
        except:
            row_ = 0
        try:
            col_ = int(df.loc[:,phon[0]].sum())
        except:
            col_ = 0
        abs_freq = row_+col_
        product_l.append((phon[0], phon[1], row_))
    
    return product_l

def contingency_table(data):
    df = pd.DataFrame({'phone':[i[0] for i in data], 'matches': [i[1] for i in data],
                                 'non-matches': [i[2]-i[1] for i in data], 'total': [i[2] for i in data]})
    df['pct']= df['matches'] / df['total'] * 100
    df = df.fillna(0)
    df = df.sort_values(by=['pct'], ascending=False)
    
    return df

contingency_table(get_freqs(handle_df(path_)))
