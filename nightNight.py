#!/usr/bin/env python
import os
import random
import subprocess
import argparse
import platform
import json

def setVolume(volume):
  if platform.system() == 'Darwin':
    subprocess.Popen('osascript -e "set Volume ' + str(volume) + '"', shell=True)
  else:
    subprocess.Popen('pactl set-sink-volume 0 ' + str(volume *10) + '%', shell=True)

def runvlc(file1, file2, file3):
  if platform.system() == 'Darwin':
    subprocess.Popen([
      "/Applications/VLC.app/Contents/MacOS/VLC",
      "--play-and-exit",
      "--fullscreen",
      file1,
      file2,
      file3])
  else:
    subprocess.Popen([
      "vlc",
      "--play-and-exit",
      "--fullscreen",
      file1,
      file2,
      file3])




def getSettingsFileName():
  return os.path.join(os.getenv("HOME"), ".night_night_settings")

def getFiles(entry):
  toReturn = []
  if os.path.isdir(entry):
    for file in os.listdir(entry):
      toReturn.extend(getFiles(entry+"/"+file))
  elif "ehthumbs.db" not in entry and "Thumbs.db" not in entry:
    toReturn.append(entry)
  return toReturn

def playFiles(potentialFiles, volume):
  setVolume(volume)
  pos1 = random.randint(0,len(potentialFiles)-1)
  pos2 = random.randint(0,len(potentialFiles)-1)
  pos3 = random.randint(0,len(potentialFiles)-1)
  print potentialFiles[pos1]
  print potentialFiles[pos2]
  print potentialFiles[pos3]
  runvlc(potentialFiles[pos1], potentialFiles[pos2], potentialFiles[pos3])
  if platform.system() == 'Dawin':
    subprocess.Popen("osascript -e 'tell application \"VLC\"' -e 'activate' -e 'end tell'", shell=True)



def startNightNight(directory, volume):
  potentialFiles = getFiles(directory)
  playFiles(potentialFiles, volume)


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--towatch', default="default")
args = parser.parse_args()



try:
  settingsFile = open(getSettingsFileName(), 'r')
except IOError as e:
  print "Couldn't open settings file"
  exit(1)

settings = json.loads(settingsFile.read())
watch_options = settings['watch_options']
towatch = None
for watch_option in watch_options:
  if watch_option['name'] == args.towatch:
    towatch = watch_option['directory']
    break

if towatch != None:
  startNightNight(towatch, settings["volume"])
else:
  print "No watch option with the name %s." % args.towatch
  exit(1)
