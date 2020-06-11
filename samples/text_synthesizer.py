'''
   Python sample program that uses MapTextSynthesizer through Ctypes.
   Copyright (C) 2018 Liam Niehus-Staab, Ziwen Chen, Benjamin Gafford

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import cv2
import sys
import os
import numpy as np
import time

# for Ctypes usage, see tensorflow/generator/data_synth.py
sys.path.insert(0, '../tensorflow/generator/') #insert path to find data_synth
from data_synth import data_generator as data_generator

# Global Variable definition
mts = data_generator("config.txt")
pause=200 #starting miliseconds between images



### GUI Callback functions

def updateTime(x):
    global pause
    pause=x


    
### GUI window functions

def initWindows():
    global mts
    global pause
    # create window to visualize the images
    cv2.namedWindow('Text Synthesizer Demo',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Text Synthesizer Demo',1000,500)
    cv2.moveWindow('Text Synthesizer Demo',100,100)
    
    # create trackbar so the pause time can be dynamically adjuseted
    cv2.createTrackbar('Pause ms','Text Synthesizer Demo',int(pause),
                       500,updateTime)

def updateTrackbars():
    global pause
    cv2.setTrackbarPos('Pause ms','Text Synthesizer Demo',int(pause))

def guiLoop():
    global mts
    global pause
    k=''
    #run the gui image show loop until user presses 'q'
    while ord('q')!=k:
        if pause<500:
            # generate sample and store data
            caption,image = next( mts )
            
            # print sample information
            print(caption)
            
            # show the sample image
            cv2.imshow('Text Synthesizer Demo',image)
            
        k=cv2.waitKey(pause+1)


def benchmark(num_iters):
    global mts
    k=0
    print("Running benchmark", end=' ')
    sys.stdout.flush()
    start = time.time()
    #run the benchmark for num_iters images
    while k < num_iters:
        k += 1
        # generate sample and store data
        caption,image = next( mts )
        if num_iters/10 % k == 0:
            print(".", end=' ')
            sys.stdout.flush()
    end = time.time()
    print(".")
    runtime = end-start
    print("Total Runtime: {} seconds".format(runtime))
    print("Images Generated: {}".format(num_iters))
    print("Production Rate: {} Hz".format(num_iters/runtime)) 
        
# main; run the gui
if __name__=='__main__':
    # init gui window info
    initWindows()
    updateTrackbars()
    # generate and show MTS images
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        num_iters = 10000
        benchmark(10000)
    else:
        guiLoop()
