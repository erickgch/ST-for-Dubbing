# This script analyzes frequency and intensity peak values (+/- 2 stdevs from the mean).
# More concretely, it looks for pairs of aligned segments with the same number of peaks. 

# Just complete the paths to the folders containing the segment files and run it.

import pandas as pd
import glob
import math, statistics
import csv
import re

path_on= # "/PATH/heroes*.csv"
path_off= # "/PATH/heroes*.csv"
path_mix= # "/PATH/heroes*.csv"

path_on_sp = # "/PATH/heroes*.csv"
path_off_sp = # "/PATH/heroes*.csv"
path_mix_sp = # "/PATH/heroes*.csv"

# dat function returns all the frequency and intensity values for each word for each segment per path

def dat_function(path):
    freq_list = []
    int_list = []

    for fname in glob.glob(path):
        df = pd.read_csv(fname, delimiter='|')
        for index, row in df.iterrows():
            if abs(row.f0_mean) > 0:
                freq_list.append(row.f0_mean)
            if abs(row.i0_mean) > 0:
                int_list.append(row.i0_mean)
            else:
                pass
    return freq_list, int_list


'''
# compute mean and stdev for each screen category

on_res = dat_function(path_on)
off_res = dat_function(path_off)
mix_res = dat_function(path_mix)
on_sp_res = dat_function(path_on_sp)
off_sp_res = dat_function(path_off_sp)
mix_sp_res = dat_function(path_mix_sp)

pairs = [(on_res, on_sp_res), (off_res, off_sp_res), (mix_res, mix_sp_res)]

all_eng = (on_res[0] + off_res[0] + mix_res[0], on_res[1] + off_res[1] + mix_res[1])
all_spa = (on_sp_res[0] + off_sp_res[0] + mix_sp_res[0], on_sp_res[1] + off_sp_res[1] + mix_sp_res[1])

#absolute values
freq_abs_mean = statistics.mean(all_eng[0])
int_abs_mean = statistics.mean(all_eng[1])

print('mean freq ',freq_abs_mean)
print('mean int ',int_abs_mean)

freq_abs_stdev = statistics.stdev(all_eng[0])
int_abs_stdev = statistics.stdev(all_eng[1])

#screen-dep values
freq_on_mean = statistics.mean(on_res[0])
freq_off_mean = statistics.mean(off_res[0])
freq_mix_mean = statistics.mean(mix_res[0])

freq_on_stdev = statistics.stdev(on_res[0])
freq_off_stdev = statistics.stdev(off_res[0])
freq_mix_stdev = statistics.stdev(mix_res[0])

int_on_mean = statistics.mean(on_res[1])
int_off_mean = statistics.mean(off_res[1])
int_mix_mean = statistics.mean(mix_res[1])

int_on_stdev = statistics.stdev(on_res[1])
int_off_stdev = statistics.stdev(off_res[1])
int_mix_stdev = statistics.stdev(mix_res[1])
'''

import pandas as pd
import glob
import math, statistics
import csv
import re

path_on= # "/PATH/heroes*.csv"
path_on_sp = # "/PATH/heroes*.csv"

path_off= # "/PATH/heroes*.csv"
path_off_sp = # "/PATH/heroes*.csv"

path_mix= # "/PATH/heroes*.csv"
path_mix_sp = # "/PATH/heroes*.csv"

# this func. gets the word, (shortened)id, f0_mean and i0_mean for each word for each segment file in the path
def pre_peak_finder(path):
    final_list = []
    for fname in glob.glob(path):
        temp_l = ()
        temp_seg = []
        t_df = pd.read_csv(fname, delimiter='|')
        for index, row in t_df.iterrows():
            id_i = str(row.id[:13])+str(row.id[24:])
            temp_l = (row.word, id_i, row.f0_mean, row.i0_mean)
            temp_seg.append(temp_l)
            temp_l = ()
        final_list.append(temp_seg)
        temp_seg = []
    return final_list

# calling pre_peak_finder func. Use these pairs as input for peak_finder func.

a = pre_peak_finder(path_on)
b = pre_peak_finder(path_on_sp)

m = pre_peak_finder(path_off)
n = pre_peak_finder(path_off_sp)

x =  pre_peak_finder(path_mix)
y =  pre_peak_finder(path_mix_sp)

def segment_peak_finder(f):
    freq_peaks = []
    int_peaks = []
    ids_freq = []
    ids_int = []
    
    for seg in f:
        for w in seg:
            # frequency peaks
            if w[2] >= (freq_abs_mean + 2*freq_abs_stdev) or w[2] <= (freq_abs_mean - 2*freq_abs_stdev):
                if seg not in freq_peaks:
                    freq_peaks.append(seg)
                else:
                    pass
                if w[1] not in ids_freq:
                    ids_freq.append([w[1], w[0], w[2], w[3]])
                else:
                    pass
            # intensity peaks
            if w[3] >= (int_abs_mean + 2*int_abs_stdev) or w[3] <= (int_abs_mean - 2*int_abs_stdev):
                int_peaks.append(seg)
                if w[1] not in ids_int:
                    ids_int.append([w[1], w[0], w[2], w[3]])
                else:
                    pass
            else:
                pass
            
    return freq_peaks, int_peaks, ids_freq, ids_int

segs_en_on = segment_peak_finder(a)
segs_spa_on = segment_peak_finder(b)

segs_en_off = segment_peak_finder(m)
segs_spa_off = segment_peak_finder(n)

segs_en_mix = segment_peak_finder(x)
segs_spa_mix = segment_peak_finder(y)

import pandas as pd

def df_maker(data):
    my_df_freq = pd.DataFrame({'segment': [i[0].split('.word')[0] for i in data[2]], 
                          'word_id': [i[0].split('.word')[1] for i in data[2]], 
                          'word': [i[1] for i in data[2]], 'frequency': [i[2] for i in data[2]],
                         'intensity': [i[3] for i in data[2]]})
    
    my_df_int = pd.DataFrame({'segment': [i[0].split('.word')[0] for i in data[3]], 
                          'word_id': [i[0].split('.word')[1] for i in data[3]], 
                          'word': [i[1] for i in data[3]], 'frequency': [i[2] for i in data[3]],
                         'intensity': [i[3] for i in data[3]]})
    
    return my_df_freq, my_df_int

# obtaining common elements between paired datasets

def commonalities(a, b):
        
    common_freq_ = set.intersection(set(a[0].segment), set(b[0].segment))
    common_int_ = set.intersection(set(a[1].segment), set(b[1].segment))
    
    return common_freq_, common_int_

print('on/freq ',len(commonalities(df_maker(segs_en_on), df_maker(segs_spa_on))[0]))
print('on/int ',len(commonalities(df_maker(segs_en_on), df_maker(segs_spa_on))[1]))

print('off/freq ',len(commonalities(df_maker(segs_en_off), df_maker(segs_spa_off))[0]))
print('off/int ',len(commonalities(df_maker(segs_en_off), df_maker(segs_spa_off))[1]))

print('mix/freq ',len(commonalities(df_maker(segs_en_mix), df_maker(segs_spa_mix))[0]))
print('mix/int ',len(commonalities(df_maker(segs_en_mix), df_maker(segs_spa_mix))[1]))



