from scipy.io import wavfile
import os

path = "penta"
for filename in os.listdir(path):
    if ".wav" in filename:
        fs, array = wavfile.read(path+"/"+filename)
        zero_num = 0
        i = 0
        while True:
            if (array[i] == array[0]).any():
                zero_num+=1
                i+=1
            else:
                break
        array = array[zero_num:]
        wavfile.write(path+"/"+filename, 44100, array)
        print (path+"/"+filename, " done!")

print ("")
print ("finished!")
