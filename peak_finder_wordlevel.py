# This script looks for words with peak frequency and intensity values. It returns the word, 
# id of the segment it belongs to, and freqneucy and intensity values.

# Just complete with the paths to the folders containing the segment files and execute.

import pandas as pd
import glob
import math, statistics
import csv
import re

path_on= # /PATH/heroes*.csv"
path_on_sp = #/PATH/heroes*.csv"
path_off = #  /PATH/heroes*.csv"
path_off_sp = # /PATH/heroes*.csv"
path_mix = # /PATH/heroes*.csv"
path_mix_sp = # /PATH/heroes*.csv"

# this func. gets the word, (shortened)id, f0_mean and i0_mean for each word for each segment file in the path
def pre_peak_finder(path):
    final_list = []
    for fname in glob.glob(path):
        temp_l = ()
        t_df = pd.read_csv(fname, delimiter='|')
        for index, row in t_df.iterrows():
            id_i = str(row.id[:13])+str(row.id[24:])
            temp_l = (row.word, id_i, row.f0_mean, row.i0_mean)
            final_list.append(temp_l)
            temp_l = ()
    return final_list

# calling pre_peak_finder function. Use these pairs as input for peak_finder function.

on_en = pre_peak_finder(path_on)
on_sp = pre_peak_finder(path_on_sp)

off_en = pre_peak_finder(path_off)
off_sp = pre_peak_finder(path_off_sp)

mix_en =  pre_peak_finder(path_mix)
mix_sp =  pre_peak_finder(path_mix_sp)

# peak_finder returns, for both frequency and intensity, a df with words whose values go beyond/below the threshold (2 stdev)
def peak_finder(eng_f, spa_f):
    my_df_eng = pd.DataFrame({'word': [i[0] for i in eng_f], 'id': [i[1] for i in eng_f], 'frequency': [i[2] for i in eng_f],
                             'intensity': [i[3] for i in eng_f]})
    my_df_spa = pd.DataFrame({'word': [i[0] for i in spa_f], 'id': [i[1] for i in spa_f], 'frequency': [i[2] for i in spa_f],
                             'intensity': [i[3] for i in spa_f]})
    my_df_eng = my_df_eng.dropna()
    my_df_spa = my_df_spa.dropna()
    
    def peaks(df):
        freq_peaks_ = df.loc[df['frequency'] >= freq_abs_mean + 2*freq_abs_stdev]
        freq_peaks_l_ = df.loc[df['frequency'] <= freq_abs_mean - 2*freq_abs_stdev]
        freq_peaks_ = freq_peaks_.append(freq_peaks_l_)

        int_peaks_ = df.loc[df['intensity'] >= int_abs_mean + 2*int_abs_stdev]
        int_peaks_l_ = df.loc[df['intensity'] <= int_abs_mean - 2*int_abs_stdev]
        int_peaks_ = int_peaks_.append(int_peaks_l_)
        
        return freq_peaks_, int_peaks_
    
    eng_proc = peaks(my_df_eng)
    spa_proc = peaks(my_df_spa)

    common_freq_ = set.intersection(set(eng_proc[0].id), set(spa_proc[0].id))
    common_int_ = set.intersection(set(eng_proc[1].id), set(spa_proc[1].id))

    peaks_df_freq = pd.concat([
    eng_proc[0][eng_proc[0].id.isin(common_freq_)],
    spa_proc[0][spa_proc[0].id.isin(common_freq_)]]).sort_values(by='id')
    
    peaks_df_int = pd.concat([
    eng_proc[1][eng_proc[1].id.isin(common_int_)],
    spa_proc[1][spa_proc[1].id.isin(common_int_)]]).sort_values(by='id')
    
    return peaks_df_freq, peaks_df_int


# writing csv files with results

peak_finder(a,b)[0].to_csv('frequency_peaks_on.csv', index=False)
peak_finder(a,b)[1].to_csv('intensity_peaks_on.csv', index=False)

peak_finder(m,n)[0].to_csv('frequency_peaks_off.csv', index=False)
peak_finder(m,n)[1].to_csv('intensity_peaks_off.csv', index=False)

peak_finder(x,y)[0].to_csv('frequency_peaks_mixed.csv', index=False)
peak_finder(x,y)[1].to_csv('intensity_peaks_mixed.csv', index=False)
