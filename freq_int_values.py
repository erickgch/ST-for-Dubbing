# This script returns a dataframe with the mean StdDev of f0 and intensity values per prosodic phrase, in addition to a comparison of these values between source and target.

import pandas as pd
import math, statistics
import glob
import csv
import re

#path_ must be a folder with a collection of files
path_ = input()
path_2 = input()
df1_name = input()
df2_name = input()

# function to obtain number of prosodic phrases per segment and means,std devs of frequency and intensity for each phrase.
def fq_int_calc(path, tag='x'): # tag = on/off/mixed
    final_value_list = []
    final_pcount_list = []
    for fname in glob.glob(path):
        df = pd.read_csv(fname, delimiter='|')
        # fq_int = list containing mean freq and mean int for each segment. 
        #          It is a list of lists (prosodic phrases) of tuples (words).
        fq_int = []
        temp_l_ = []
        w_count = 0
        phrase_count = 0
        fname_ = ''.join(re.findall(r'(s\d.+)\.', fname))
        
        # phrases are delimited by silences longer than 0.25 secs or periods.
        for index, row in df.iterrows():
            w_count += 1
            if w_count == len(df):
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
                fq_int.append(temp_l_)
                temp_l_ = []
                phrase_count += 1        
            elif(float(row.pause_after)) >= 0.25:
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
                fq_int.append(temp_l_)
                temp_l_ = []
                phrase_count += 1
            elif row['punctuation_after'] == '.':
                # periods, besides silences over 0.25s, are used to delimit phrases
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
                fq_int.append(temp_l_)
                temp_l_ = []
                phrase_count += 1
            else:
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
        final_pcount_list.append([fname_,str(len(fq_int))])

        # This part computes the length - in number of words - of each prosodic phrase
        n = 0 # to assign the prosodic phrase number to each row in the df
        for i in fq_int:
            temp_ = []
            temp_2 = []
            for k in i:
                temp_.append(k[0])
                temp_2.append(k[1])
            
            n = n+1
            try:
                name = (fname_+str(n))
                freq_mean = statistics.mean(temp_)
                freq_stdev = statistics.stdev(temp_)
                freq_stdev_cent = 1200*math.log2((freq_mean+freq_stdev)/freq_mean)
                int_mean = statistics.mean(temp_2)
                int_stdev = statistics.stdev(temp_2)
                
                vl = [name, freq_mean, freq_stdev, freq_stdev_cent, int_mean, int_stdev, str(tag)]
            # if segments consist of a single word, Stdev cannot be calculated, thus a value of 0 is assigned.
            except:
                name = (fname_+str(n))
                freq_mean = k[0]
                freq_stdev = 0
                int_mean = k[1]
                int_stdev = 0
    
                vl = [fname_, k[0], 0, 0, k[1], 0, str(tag)]
        final_value_list.append(vl)
        
    return final_value_list

#write csv from fq_int_calc data
def csv_output(data, csv_name):
    with open((str(csv_name)+'.csv'), "w", newline='',encoding='utf-8') as file_:
            csv_out=csv.writer(file_)
            csv_out.writerow(['file_name','freq_mean', 'freq_stdev_hz', 'freq_stdev_cent', 'int_mean', 'int_stdev', 'on/off'])
            for row in data:
                csv_out.writerow(row)
    return file_

def create_df(eng_data, spa_data):
    import numpy as np
    import pandas as pd
        #eng_data, spa_data are csv files created using the fq_int_calc function
    df_spa = pd.read_csv(spa_data)
    df_eng = pd.read_csv(eng_data)

    #dataframe with relevant data
    df_diff = pd.DataFrame({'file_name': df_eng.file_name, 'freq_eng': df_eng.freq_stdev_cent, 'freq_spa': df_spa.freq_stdev_cent,
                           'int_eng': df_eng.int_stdev, 'int_spa': df_spa.int_stdev})
    #removing anomalous phrases (e.g. 0 freq/int)
    df_diff = df_diff.drop(df_diff[df_diff.freq_eng < 1].index)
    df_diff = df_diff.drop(df_diff[df_diff.freq_spa < 1].index)
    df_diff = df_diff.drop(df_diff[df_diff.int_eng < 1].index)
    df_diff = df_diff.drop(df_diff[df_diff.int_spa < 1].index)
    #new columns
    df_diff['diff_freq_in_cents'] = np.where(df_diff['freq_eng'] == df_diff['freq_spa'], 0, df_diff['freq_eng'] - df_diff['freq_spa'])
    df_diff['diff_freq_proportion'] = ((df_diff.freq_eng / df_diff.freq_spa) - 1)
    df_diff['winner_freq'] = np.where(df_diff['freq_eng'] > df_diff['freq_spa'], 'ENG', 'SPA')
    df_diff['diff_int_db'] = np.where(df_diff['int_eng'] == df_diff['int_spa'], 0, df_diff['int_eng'] - df_diff['int_spa'])
    df_diff['winner_int'] = np.where(df_diff['int_eng'] > df_diff['int_spa'], 'ENG', 'SPA')
    
    return df_diff

csv_output(fq_int_calc(path_), df1_name)
csv_output(fq_int_calc(path_2), df2_name)

create_df(df1_name+'.csv', df2_name+'.csv')



