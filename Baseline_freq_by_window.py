import pandas as pd
import numpy as np
from scipy import signal

filename = 'Post_Baseline_farihaEC.csv'

save_file_name = filename[:-4] + '_processed.csv'

data = pd.read_csv(filename)

feedback_channel = np.array(data['8'])

Fs = 500
wL = 4 * Fs
n = 0
baseline_mean_frequency = []

buffer_data = feedback_channel[0:2000]

buffer_data = buffer_data.tolist() 

for window in range(len(feedback_channel) - 2000):
    
    pwelch = signal.welch(buffer_data, fs=Fs, window='hanning', nperseg=wL, noverlap=wL/2, nfft=wL) #replace 'hanning' with 'hann' if you are using the latest version (3.11) of python. 
    
    baseline_beta = pwelch[1][int(wL*15/Fs) : int((wL*20/Fs)) + 1] # +1 due to python run till last index -1  
    
    baseline_mean_frequency.append(np.mean(baseline_beta))
    
    buffer_data.pop(0)
    
    buffer_data.insert(1999, feedback_channel[2000+n])

    n += 1
 

df = pd.DataFrame(baseline_mean_frequency, columns =['Mean Frequencies'])

df.to_csv(save_file_name)



    
