#!/usr/bin/python

import tkinter
import tkinter.messagebox
import tkinter.font
import time
import sys 
import _thread
import threading
import datetime

from tkinter import *
from tkinter.ttk import Style
from time import strftime
from tkFontChooser import askfont
from sys import platform
from datetime import datetime

# Initialize root window
top = tkinter.Tk()

# Always on top
top.wm_attributes("-topmost", 1)

# Style chooser
style = Style(top)
if "win" == platform[:3]:
    style.theme_use('vista')
elif "darwin" in platform:
    style.theme_use('clam')
else:
    style.theme_use('clam')
bg = style.lookup("TLabel", "background")
top.configure(bg=bg)

# Initialize variables
timer_stop = 0 
scheduleMatrix = [[]]
totalNumSchedules = 0

# Load the schedule into an two dimensional array
def loadScheduleData():  
   global totalNumSchedules
   # Look for file named schedule.dat
   textFile = open("schedule.dat", "r")
   lines = textFile.readlines()
   sCount = 0

   # Get number of lines from file
   with open('schedule.dat') as f:
       totalNumSchedules = sum(1 for _ in f)

   global scheduleMatrix
   scheduleMatrix = [["" for x in range(4)] for y in range(totalNumSchedules)] 

   for schData in lines:
        scheduleEntry = schData.split('>')
        scheduleEntryLength = len(scheduleEntry)
        if scheduleEntryLength > 1 :
            scheduleEntryArray = scheduleEntry[0].split('-') 
            scheduleStartTime = scheduleEntryArray[0]
            scheduleEndTime = scheduleEntryArray[1]
            scheduleText = scheduleEntry[1]
            scheduleMatrix[sCount][0] = scheduleStartTime
            scheduleMatrix[sCount][1] = scheduleEndTime
            scheduleMatrix[sCount][2] = scheduleText.strip()
            if scheduleEntryLength == 3 :
                 scheduleMatrix[sCount][3] = scheduleEntry[2]
            sCount += 1


# Main function
def startCountDown():
   try:
      _thread.start_new_thread(startTimer , ("Thread-1", 2, ) ) 
   except:
      tkinter.messagebox.showinfo("Error", "Unable to start thread")


def startTimer( threadName, delay):
   global timer_stop
   global scheduleMatrix
   loadScheduleData()
   time_start = time.time()
   hours = 0
   seconds = -1 
   minutes = 0
   prev_second = 0
   current_second = 0
   currentScheduleText = ""

   var3.set(strftime("%H") + ": "  + strftime("%M") + ": " + strftime("%S"))
   currentScheduleText = getCurrentSchedule(strftime("%H"),strftime("%M"))
   if currentScheduleText:
      var4.set(currentScheduleText)

   while True:
       try:
           current_second = strftime("%S")
           time.sleep(500/1000.0)
           if prev_second != current_second:
               seconds += 1
               prev_second = current_second

               if seconds == 60: 
                   minutes += 1
                   seconds = 0
                   currentScheduleText = getCurrentSchedule(strftime("%H"),strftime("%M"))
                   if currentScheduleText:
                       var4.set(currentScheduleText)

               if minutes == 60: 
                   hours += 1
                   minutes = 0 
                   

               var1.set(("0"+str(hours) if hours < 10 else str(hours)) + ": " + ("0"+str(minutes) if minutes < 10 else str(minutes)) + ": " + ("0"+str(seconds) if seconds < 10 else str(seconds)))
               var2.set(strftime("%H") + ": " + strftime("%M") + ": " + strftime("%S"))

           if timer_stop == 1:
               timer_stop = 0
               break
       except KeyboardInterrupt:
           break


def stopTimer():
   global timer_stop
   timer_stop = 1


def getCurrentSchedule(hour,minutes):
   global scheduleMatrix
   global totalNumSchedules
   scheduleTxt = "No matching schedules"
   currTime = (int(hour)*100) + int(minutes)
   for i in range(totalNumSchedules):
       startTimeComponents = scheduleMatrix[i][0].split(":")
       endTimeComponents = scheduleMatrix[i][1].split(":")
       if (currTime >= (int(startTimeComponents[0])*100)+int(startTimeComponents[1]) 
           and currTime <= (int(endTimeComponents[0])*100)+int(endTimeComponents[1])):
           scheduleTxt = scheduleMatrix[i][2] +"till "+ scheduleMatrix[i][1]
           break
   return scheduleTxt




cFont1 = tkinter.font.Font(family="sans-serif", size=16)

var1 = StringVar()
label1 = Label( top, textvariable=var1, relief=FLAT ,font=cFont1)
label1.grid(row=0,column=0)
var2 = StringVar()
label2 = Label( top, textvariable=var2, relief=FLAT ,font=cFont1)
label2.grid(row=1,column=0)
var3 = StringVar()
label3 = Label( top, textvariable=var3, relief=FLAT ,font=cFont1)
label3.grid(row=2,column=0)
var4 = StringVar()
cFont2 = tkinter.font.Font(family="sans-serif", size=14)
label4 = Label( top, textvariable=var4, relief=GROOVE ,font=cFont2, wraplength=180)
label4.grid(row=3,column=0, columnspan=2)


def chooseFont():
    # open the font chooser and get the font selected by the user
    font = askfont(top)
    # font is "" if the user has cancelled
    if font:
        # spaces in the family name need to be escaped
        # font['family'] = font['family'].replace(' ', '\ ')
        cFont1 = tkinter.font.Font(family="%(family)s" % font, size="%(size)i" % font)
        label1.configure(font=cFont1)
        label2.configure(font=cFont1)
        label3.configure(font=cFont1)
        optimizedSize=int("%(size)i"%font)
        optimizedSize-=2
        cFont2 = tkinter.font.Font(family="%(family)s" % font, size=optimizedSize)
        label4.configure(font=cFont2)



B1 = tkinter.Button(top, text ="Start", command = startCountDown)
B1.grid(row=0,column=1)
B2 = tkinter.Button(top, text ="Stop", command = stopTimer)
B2.grid(row=1,column=1)
B3 = tkinter.Button(top, text ="Font", command = chooseFont)
B3.grid(row=2,column=1)

top.title("Schedule Tracker")
top.mainloop()
