from pylsl import StreamInlet, resolve_stream
import numpy as np
import pandas as pd
from scipy import signal
import time
import vlc
import sys

complete_nf_mean_frequencies = []
complete_samples = []
current_data_sample = []
time_stamp = []
NFB_reached = []

name = input("Enter user name (Same as used for baseline recording): ")

NF_time = int(input("Enter the time duration for NF session: "))

NFB_Day = input("Enter Neurofeedback Day Number: ")

Session_no = input("Enter Session Number: ")

NF_file_name = 'NF' + NFB_Day + '_Ses' + Session_no + '_' + name + ".csv"

baseline_raw_array = np.transpose(np.array(pd.read_csv('User Data/Pre_Baseline_' + name + '.csv')))

Fs = 500
wL = 4 * Fs
nf_channel = 2

pwelch = signal.welch(baseline_raw_array[nf_channel], fs=Fs, window='hanning', nperseg=wL, noverlap=wL/2, nfft=wL)

baseline_beta1 = pwelch[1][int(wL*12/Fs) : int((wL*15/Fs)) + 1] # +1 due to python run till last index -1  

baseline_mean_frequency = np.mean(baseline_beta1)

print("Baseline data processing ended")

print("Waiting....")

print("Starting Neurofeedback in next 10 seconds..")

time.sleep(10)

media = vlc.MediaPlayer("NF Video.mp4")
#media.audio_set_mute(True)

check = True
#in_data_check = True # condition for initial 4 seconds data check
try:
        
    # first resolve an EEG stream on the lab network
    print("Starting Realtime NFB")
    print("looking for an EEG stream...")
    
    streams = resolve_stream('type', 'EEG')
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    t1 = time.time()
    t3 = time.time()
    realtime_mean_frequency = 0
    first_play = 1
    
    while check:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
        t2 = time.time()
        sample, timestamp = inlet.pull_sample()
        time_stamp.append(timestamp)
        complete_samples.append(sample) # this have entire data for csv file 
        
        if (t2-t3<=0.4):#time for computation of 400 ms data
            current_data_sample.append(sample[nf_channel])#index value should be change with respect to NFB Channel
            #print("cs")
                    
        else:            
            t3 = time.time() 
            #print ("time up")
            realtime_data_in_array = np.array(current_data_sample)
            #realtime_frequency = signal.sosfilt(sos1, realtime_data_in_array)
            
            Nperseg = 50*2
            Noverlap=(50*2)/2
            Nfft=50*2
            
            if (t2-t1 >= NF_time):
                Nperseg = len(realtime_data_in_array)
                Noverlap=0
                Nfft=len(realtime_data_in_array)

            real_pwelch = signal.welch(realtime_data_in_array, fs=50, window='hanning', nperseg=Nperseg, noverlap=Noverlap, nfft=Nfft)
                                   
            real_beta1 = real_pwelch[1][int(Nfft*12/Fs) : int((Nfft*15/Fs)) + 1] # +1 due to python run till last index -1 
            
            realtime_mean_frequency = np.mean(real_beta1) # having final data
            
            complete_nf_mean_frequencies.append(realtime_mean_frequency)
            #a = current_data_sample
            current_data_sample = []
            
        if(first_play == 1):
            first_play = 2
            media.play()    
            print("first")
       
        print (t2-t1)
        if realtime_mean_frequency  > baseline_mean_frequency:
            media.play()
            NFB_reached.append(1)
            print("Excelent! You are doing great")
                        
        else:
            
             print("You are going wrong.. ")
             media.pause()
             NFB_reached.append(0)
        #print(np.shape(complete_samples)[0])
        #if (np.shape(complete_samples)[0] >= nf_time*500):
        if (t2-t1 >= NF_time):# total time for nf session
        
            print (t2-t3)
            media.pause()
            check = False
            media.stop()
            
            print("Neurofeedback trial have been completed")
            
            NF_time_df = pd.DataFrame((time_stamp), columns = ['Time Stamps'])
            sample_df = pd.DataFrame(complete_samples)
            NFB_Data_df = pd.concat((NF_time_df,sample_df), axis =1)
            NFB_Data_df.to_csv('User Data/' + NF_file_name)
            
            Current_df = pd.DataFrame((current_data_sample), columns = [str(nf_channel)])
            NFB_frequency_df = pd.DataFrame((complete_nf_mean_frequencies), columns = ['NFB Mean Frequency'])
            Performance_df = pd.DataFrame((NFB_reached), columns = ['NFB_Score'])
            other_data_df = pd.concat((Current_df,NFB_frequency_df,Performance_df), axis =1)
            other_data_df.to_csv('User Data/' + 'NF_details_' + name + '.csv' )
            
                                   
except KeyboardInterrupt as e:
        print("Ending program")
        raise e



