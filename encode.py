import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import csv
import os
import threading
import time
import re
#from wand.image import Image

def encodeImages ():
  # this will encode the images with the correct 
  pathToWatch = "/media/scratch/images"
  before = dict ([(f, None) for f in os.listdir (pathToWatch)])
  while (1):
#    time.sleep (10)
    after = dict ([(f, None) for f in os.listdir (pathToWatch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: print "Added: ", ", ".join (added)
    if removed: print "Removed: ", ", ".join (removed)
    for i in added:
       matchObj = re.match(r'image(.*)\.png', i, re.M|re.I)
       if (matchObj):
         frameNo = matchObj.group (1)
#      with Image (filename="/media/scratch/images/" + i) as img:
#        img.save (filename="/media/scratch/newImages/" + i)
#        os.remove ("/media/scratch/images/" + i)
    before = after

def addLogo (name, fileIn, fileOut):
  PILImage = Image.open ("rjamlogo.png")

  width, height = PILImage.size
  dpi = 300
  font_size = 20
  font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 
                         int(dpi * font_size / 72.0))

  draw = ImageDraw.Draw(PILImage)

  text = name
  text_width, text_height = font.getsize(text)
  draw.text((260, height - 50 - text_height), 
      text, fill='black', font=font)

  rjamLogo = cv2.cvtColor(np.array(PILImage), cv2.COLOR_RGB2BGR)

  cap = cv2.VideoCapture(fileIn)

  outputVideo = cv2.VideoWriter()

  outputVideo.open(fileOut, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), 25, (1920,1080), True)

  writeFrame = ""
  ret = True
  timestamp = 0

  while(ret == True):
      ret, frame = cap.read()
      timestamp = cap.get (cv2.cv.CV_CAP_PROP_POS_MSEC)
#      print (timestamp)
      if (ret == True):
        writeFrame = frame
        height, width, depth = frame.shape

        xPos = frame.shape[0] - rjamLogo.shape[0]

        logoImage = np.zeros((height,width,3), np.uint8)
        blackImage = np.zeros ((145, 1920,3), np.uint8)
        logoImage[xPos:rjamLogo.shape[0]+xPos,:rjamLogo.shape[1]] = blackImage
        logoImage[xPos:rjamLogo.shape[0]+xPos,:rjamLogo.shape[1]] = rjamLogo

        fade = timestamp / 1000
        if (fade > 1):
          fade = 1
        if (timestamp > 29000):
          fade = (30000 - timestamp) / 1000
        if (timestamp < 30000):
          dst = cv2.addWeighted (writeFrame, 1, logoImage, fade, 0)
        else:
          dst = writeFrame
        outputVideo.write (dst)

  cap.release()

sourceFile = sys.argv[2]

file = open (sys.argv[1], "r")
reader = csv.reader (file)
for row in reader:
  personName = row[0]
  start = row[1]
  end = row[2]
  length = float(end) - float(start)

  cmdLine = "avconv -i " + sourceFile + " -ss " + start + " -t " + str(length) + " -f mpegts -r 25 -vf yadif -b:v 40M /media/scratch/tmp/" + personName + ".ts"
  os.system (cmdLine)
  cmdLine = "avconv -i /media/scratch/tmp/" + personName + ".ts /media/scratch/tmp/" + personName + ".wav"
  os.system (cmdLine)

#  encodeThread = threading.Thread (target=encodeImages)
#  encodeThread.start ()
#  cmdLine = "avconv -i /media/scratch/tmp/" + personName + ".ts -q:v 1 /media/scratch/images/image%08d.png"
#  os.system (cmdLine)
#  os.exit (0)
  addLogo (personName, "/media/scratch/tmp/" + personName + ".ts", "/media/scratch/tmp/" + personName + ".avi")
  os.system ("avconv -i /media/scratch/tmp/" + personName + ".avi -b 40M -i /media/scratch/tmp/"+personName + ".wav -r 12 -b 40M -s 960x540 /media/scratch/tmp/" + personName +".mp4")
#  os.system ("HandBrakeCLI -i /media/scratch/tmp/" + personName +".mp4 -o " + personName + ".mp4 --preset High")
  os.system ("avconv -i /media/scratch/tmp/" + personName + ".mp4 -c:a copy -c:v libx264 -crf 18 -preset veryslow " + personName + ".mp4")

  os.system ("rm /media/scratch/tmp/" + personName +".avi")
  os.system ("rm /media/scratch/tmp/" + personName +".mp4")
  os.system ("rm /media/scratch/tmp/" + personName +".wav")
