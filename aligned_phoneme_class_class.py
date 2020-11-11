# This script looks at the frequency of synchronic phoneme-to-phonetic class (e.g. /p/ in ENG --> /p, m, b/ in SPA)
#and phonetic class-to-phonetic class (e.g. bilabials --> bilabials) matches for any pair of aligned segments. 
import pandas as pd

path_ = input()

def handle_df(path):
    df = pd.read_csv(path,  delimiter='\t', index_col='Phonemes')
    #clean df
    df.loc['h'] = df.loc['h'] + df.loc['h\\']
    df = df.drop(columns=['Unnamed: 0'],index=['r', 'h\\']).rename(index={'R':'r'})
    
    return df

# classes: labial consonants, labiodental consonants, dento-alveolo-postalveolar consonants, velar consonants,
#          back-round vowels, close vowels, middle vowels, open vowels
phoneme_classes = [['<p:>'],['p','b','B','m','m='],['f','v'],
                   ['d','D','t','T','dZ','s','z','S','tS','rr','r','4','n','l','l=','jj','L'],
                   ['g','G','k','N','n'],['O:','OI','U','u:', 'Q', 'V','w','@U','o','u'],['i','I','I@','i:','j'],
                   ['e','3`','E','@','@`','eI'],['6','{','a']]

def get_freqs(df):
    #phoneme frequencies in English
    
    aligned_freqs = []
    class_aligned_freqs = []

    labels = ['pause', 'labial-c', 'labiodental-c', 'dento-alveolo-postalveolar-c', 'velar-c',
             'back-round-v', 'close-v', 'mid-v','open-v']
    n = -1
    for c in phoneme_classes:
            c_temp = []
            n += 1
            for i in c:
                temp = []
                for k in c:
                    try:
                        x = (i, df.loc[i][k])
                    except:
                        x = (i,0)
                    temp.append(int(x[1]))
                    try:
                        row_ = int(df.loc[i].sum())
                    except:
                        row_ = 0
                    try:
                        col_ = int(df.loc[:,i].sum())
                    except:
                        col_ = 0
                    abs_freq = row_+col_
                aligned_freqs.append((x[0], sum(temp), abs_freq))
                c_temp.append((sum(temp),abs_freq))
                
            class_aligned_freqs.append(('class '+labels[n], sum(i[0] for i in c_temp),sum(i[1] for i in c_temp)))
    
    return aligned_freqs, class_aligned_freqs

def contingency_table(data):
    df_phones = pd.DataFrame({'phone':[i[0] for i in data[0]], 'matches': [i[1] for i in data[0]],
                                 'non-matches': [i[2]-i[1] for i in data[0]], 'total': [i[2] for i in data[0]]})
    df_phones['pct']= df_phones['matches'] / df_phones['total'] * 100
    df_phones = df_phones.fillna(0)
    df_phones = df_phones.sort_values(by=['pct'], ascending=False)
    
    df_classes = pd.DataFrame({'phone':[i[0] for i in data[1]], 'matches': [i[1] for i in data[1]],
                                 'non-matches': [i[2]-i[1] for i in data[1]], 'total': [i[2] for i in data[1]]})
    df_classes['pct']= df_classes['matches'] / df_classes['total'] * 100
    df_classes = df_classes.fillna(0)
    df_classes = df_classes.sort_values(by=['pct'], ascending=False)
    
    return df_phones, df_classes

contingency_table(get_freqs(handle_df(path_)))
