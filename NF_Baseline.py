from pylsl import StreamInlet, resolve_stream
import numpy as np
import time
import pandas as pd


#def data_acq(name, time_Duration):

name = input("Enter user name: ")

time_Duration = int(input("Enter the Baseline Recording Duration (in seconds): "))

baseline_state = input("Is it Pre or Post : ")
        
time_stamp = []
total_samples = []

check = True
##name = input("Enter your name : ")
##time_Duration = int(input("Enter time in seconds : "))
baseline_file_name = baseline_state + '_Baseline_' + name + ".csv"


try:
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    t1 = time.time()
    while check:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
        t2 = time.time()
        sample, timestamp = inlet.pull_sample()
        time_stamp.append(timestamp)
        total_samples.append(sample) 
        print(t2-t1)
        if (t2-t1 >= time_Duration):
            check = False
    time_df = pd.DataFrame((time_stamp), columns = ['Time Stamps'])
    sample_df = pd.DataFrame(total_samples)
    Data_df = pd.concat((time_df,sample_df), axis =1)
    Data_df.to_csv('User Data/' + str(baseline_file_name))
    
    #return total_samples
    
except KeyboardInterrupt as e:
    print("Ending program")
    raise e

# data_acq("name",5)
