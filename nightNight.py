#!/usr/bin/env python

"""
Copyright 2011 Kurtis L. Nusbaum

This file is part of NightNight.

NightNight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

NightNight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with NightNight.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import random
import subprocess
import argparse
import platform
import json
import re

def getVlcExecutable():
  if platform.system() == 'Darwin':
    return "/Applications/VLC.app/Contents/MacOS/VLC"
  elif platform.system() == 'Windows':
    return "C:\\Program Files\\VideoLAN\\VLC\\VLC.exe"
  else:
    return "vlc"


def setVolume(volume):
  if platform.system() == 'Darwin':
    subprocess.Popen('osascript -e "set Volume ' + str(volume) + '"', shell=True)
  elif platform.system() == 'Windows':
    # Don't know how to do this in windows yet. Someone wanna figure it out?
    pass
  else:
    subprocess.Popen('pactl set-sink-volume 0 ' + str(volume *10) + '%', shell=True)


def getSettingsFileName():
  return os.path.join(os.path.expanduser('~'), ".night_night_settings")

def getFiles(entry):
  toReturn = []
  if os.path.isdir(entry):
    for file in os.listdir(entry):
      toReturn.extend(getFiles(entry+"/"+file))
  #this regex should be configurable
  elif re.match("(.*\.avi)|(.*\.mkv)", entry):
    toReturn.append(entry)
  return toReturn

def playFiles(potentialFiles, vlc_executable, volume):
  setVolume(volume)
  pos1 = random.randint(0,len(potentialFiles)-1)
  pos2 = random.randint(0,len(potentialFiles)-1)
  pos3 = random.randint(0,len(potentialFiles)-1)
  print potentialFiles[pos1]
  print potentialFiles[pos2]
  print potentialFiles[pos3]
  subprocess.Popen([
    vlc_executable,
    "--play-and-exit",
    "-f",
    "--video-on-top",
    potentialFiles[pos1],
    potentialFiles[pos2],
    potentialFiles[pos3]])
  if platform.system() == 'Darwin':
    subprocess.Popen("osascript -e 'tell application \"VLC\"' -e 'activate' -e 'end tell'", shell=True)



def startNightNight(directory, vlc_executable, volume):
  potentialFiles = getFiles(directory)
  playFiles(potentialFiles, vlc_executable, volume)


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--towatch', default="default")
args = parser.parse_args()



try:
  settingsFile = open(getSettingsFileName(), 'r')
except IOError as e:
  print "Couldn't open settings file. Are you sure it exists?"
  exit(1)

settingsString = settingsFile.read()
settings = json.loads(settingsString)
watch_options = settings['watch_options']
towatch = None
for watch_option in watch_options:
  if watch_option['name'] == args.towatch:
    towatch = watch_option['directory']
    break

if towatch != None:
  vlc_executable = settings.get('vlc_executable', getVlcExecutable())
  startNightNight(towatch, vlc_executable,settings["volume"])
else:
  print "No watch option with the name %s." % args.towatch
  exit(1)
