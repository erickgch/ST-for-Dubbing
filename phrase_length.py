# This script looks at the length of prosodic phrases both in terms of number of words and duration
import pandas as pd
import math, statistics
import glob
import csv, re

path = input()

# function to obtain length of prosodic phrases for each segment
def phr_length(path, tag='x'): # tag = on/off/mixed
    final_value_list = []
    final_plength_list = []
    final_wlength_list = []
    
    for fname in glob.glob(path):
        df = pd.read_csv(fname, delimiter='|')

        # phr_dur = duration for each prosodic phrase
        #          It is a list of lists (prosodic phrases) of tuples (words).
        phr_dur, phr_len = [], []
        temp_l_ = []
        w_count = 0
        
        # phrases are delimited by silences longer than 0.25 secs or periods.
        for index, row in df.iterrows():
            w_count += 1
            if w_count == len(df):
                temp_l_.append(row.duration)
                phr_dur.append(sum(temp_l_))
                phr_len.append(w_count)
                temp_l_ = []      
            elif(float(row.pause_after)) >= 0.25:
                temp_l_.append(row.duration)
                phr_dur.append(sum(temp_l_))
                phr_len.append(w_count)
                temp_l_ = []
            else:
                temp_l_.append((row.duration))
        final_plength_list.append(phr_dur)
        final_wlength_list.append(phr_len)

    n = 0 # to assign the prosodic phrase number to each row in the df
    for l, m in zip(final_plength_list, final_wlength_list):
        for i, k in zip(l, m):
            n = n+1
            try:
                name = ''.join(re.findall(r'(s\d.+\d)', fname))
                name = name+'.'+str(n)
                phr_duration = i
                phr_w_length = k

                vl = [name, phr_duration, phr_w_length, str(tag)]
            # to handle phrases with 0 duration (if any)
            except:
                name = ''.join(re.findall('(s\d.+\d)', fname))
                name = name+'.'+str(n)

                vl = [name, 0, 0, str(tag)]
        
        final_value_list.append(vl)
        
    return final_value_list

#write csv output with phrase lengths
def csv_output(data, csv_name):   
    with open((str(csv_name)+'.csv'), "w", newline='',encoding='utf-8') as file_:
        csv_out=csv.writer(file_)
        csv_out.writerow(['file_name','duration', 'w_count', 'on/off'])
        for row in data:
            csv_out.writerow(row)
            
    return file_

csv_output(phr_length(path), 'test_df')



