# This script looks at the mean freq and intensity values of each segment (source and target). 
# The stdev of these variables allow for an analysis of variation in terms of intonation and loudness.

import pandas as pd
import math, statistics
import glob
import csv
import numpy

path_spa = r"C:/Users/erick/OneDrive/Desktop/MT-FBK-internship/on-off/on_spa/heroes*.csv"
path_eng = r"C:/Users/erick/OneDrive/Desktop/MT-FBK-internship/on-off/on_eng/heroes*.csv"

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
                # only periods
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
                fq_int.append(temp_l_)
                temp_l_ = []
                phrase_count += 1
            else:
                temp_l_.append((row.f0_mean_hz,row.i0_mean_db))
        final_pcount_list.append([fname[-28:-4],str(len(fq_int))])

        n = 0 # to assign the prosodic phrase number to each row in the df
        for i in fq_int:
            temp_ = []
            temp_2 = []
            for k in i:
                temp_.append(k[0])
                temp_2.append(k[1])
            
            n = n+1
            try:
                name = (fname[-28:-3]+str(n))
                freq_mean = statistics.mean(temp_)
                freq_stdev = statistics.stdev(temp_)
                freq_stdev_cent = 1200*math.log2((freq_mean+freq_stdev)/freq_mean)
                int_mean = statistics.mean(temp_2)
                int_stdev = statistics.stdev(temp_2)
                
                vl = [name, freq_mean, freq_stdev, freq_stdev_cent, int_mean, int_stdev, str(tag)]
            # if segments consist of a single word, Stdev cannot be calculated, thus a value of 0 is assigned.
            except:
                name = (fname[-28:-3]+str(n))
                freq_mean = k[0]
                freq_stdev = 0
                int_mean = k[1]
                int_stdev = 0
    
                vl = [name, k[0], 0, 0, k[1], 0, str(tag)]
        final_value_list.append(vl)
        
    return final_value_list, final_pcount_list
	


# creating csv files with the results by calling the function created above. REPEAT FOR EVERY SCREEN CATEGORY (ON/OFF/MIXED)

	# English freq, int
with open('results_frequency_intensity_eng_on.csv', "w", newline='',encoding='utf-8') as f:
        csv_out=csv.writer(f)
        csv_out.writerow(['file_name','freq_mean', 'freq_stdev_hz', 'freq_stdev_cent', 'int_mean', 'int_stdev', 'on/off'])
        for row in fq_int_calc(path_eng, 'on')[0]:
            csv_out.writerow(row)

	# Spanish freq, int
with open('results_frequency_intensity_spa_on.csv', "w", newline='',encoding='utf-8') as f:
        csv_out=csv.writer(f)
        csv_out.writerow(['file_name','freq_mean', 'freq_stdev_hz', 'freq_stdev_cent', 'int_mean', 'int_stdev', 'on/off'])
        for row in fq_int_calc(path_spa, 'on')[0]:
            csv_out.writerow(row)

	# English number of phrases
with open('num_phrases_spa_on.csv', "w", newline='',encoding='utf-8') as f:
        csv_out=csv.writer(f)
        csv_out.writerow(['file_name','num_phrases'])
        for row in fq_int_calc(path_eng)[1]:
            csv_out.writerow(row)

	# Spanish number of phrases
with open('num_phrases_spa_on.csv', "w", newline='',encoding='utf-8') as f:
        csv_out=csv.writer(f)
        csv_out.writerow(['file_name','num_phrases'])
        for row in fq_int_calc(path_spa)[1]:
            csv_out.writerow(row)

# Comparing frequency and intensity between ENG ans SPA using pandas
# on-screen

import numpy as np
import pandas as pd

eng_data = r"C:/Users/erick/OneDrive/Desktop/results_frequency_intensity_eng_on.csv" # change path
spa_data = r"C:/Users/erick/OneDrive/Desktop/results_frequency_intensity_spa_on.csv" # change path

def comparisons_df(path_src, path_trg):

	df_spa = pd.read_csv(path_trg)
	df_eng = pd.read_csv(path_src)

	#dataframe with relevant data
	df_diff = pd.DataFrame({'file_name': df_eng.file_name, 'freq_eng': df_eng.freq_stdev_cent, 'freq_spa': df_spa.freq_stdev_cent,
						   'int_eng': df_eng.int_stdev, 'int_spa': df_spa.int_stdev})

	#removing anomalous phrases (e.g. 0 freq/int)
	df_diff = df_diff.drop(df_diff[df_diff.freq_eng < 1].index)
	df_diff = df_diff.drop(df_diff[df_diff.freq_spa < 1].index)
	df_diff = df_diff.drop(df_diff[df_diff.int_eng < 1].index)
	df_diff = df_diff.drop(df_diff[df_diff.int_spa < 1].index)

	#new columns; winner = which language has the higher freq/int
	df_diff['diff_freq_in_cents'] = np.where(df_diff['freq_eng'] == df_diff['freq_spa'], 0, df_diff['freq_eng'] - df_diff['freq_spa'])
	df_diff['diff_freq_proportion'] = ((df_diff.freq_eng / df_diff.freq_spa) - 1)
	df_diff['winner_freq'] = np.where(df_diff['freq_eng'] > df_diff['freq_spa'], 'ENG', 'SPA')
	df_diff['diff_int_db'] = np.where(df_diff['int_eng'] == df_diff['int_spa'], 0, df_diff['int_eng'] - df_diff['int_spa'])
	df_diff['winner_int'] = np.where(df_diff['int_eng'] > df_diff['int_spa'], 'ENG', 'SPA')
	
	return df_diff
	
comparisons_df(eng_data, spa_data)