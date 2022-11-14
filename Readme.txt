Important Notes:

Install Anaconda Python 3.6 or 3.7
Install VLC Media Player
Bit version (either 32 bit or 64 bit) should be same for Anaconda Python and VLC Media Player
When you complete with the installation,
open "Anaconda Prompt" from the search option on the task bar.
install libraries by writing,
1- pip install python-vlc
2- pip install pylsl

Save the video (in "Neurofeedback_OE" folder) that you want to play during Neurofeedback sessions.
Video should be in MP4 format with the name "NF Video.MP4"

Please follow the steps below when you are running Neurofeedback.

1- Run Mitsar data Studio and EEG Studio Acquisition, set your EEG Montage then start recording and under "Add-on" tab, click on "LSL Outlet".

2- Minimize all windows and keep running MITSAR Softwares.

3- Open Folder "Neurofeedback_OE"

4- click on address bar, write 'cmd' and then press 'Enter'

5- Now write Python Codes as 'python file name.py'.

	for example,
		when you are starting, write 'python NF_Baseline.py'
		after completion of baseline recording
		write 'python NF.py'  

Note: Enter the same user name (same spelling and case) for both NF_Baseline.py and NF.py for each subject
