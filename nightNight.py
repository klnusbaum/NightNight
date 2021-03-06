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


DEFAULT_VIDEO_FILE_REGEX = r'(.*\.avi)|(.*\.mkv)'

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

def getFiles(entry, video_file_regex):
  toReturn = []
  for dirpath, _, files in os.walk(entry, followlinks=True):
    for f in files:
      if re.match(video_file_regex, f):
        toReturn.append(os.path.join(dirpath, f))
  if len(toReturn) < 1:
    print "Could not find any video files in \"{0}\" while using the regular expression \"{1}\".".format(entry, video_file_regex)
    exit(1)
  return toReturn


def playFiles(potentialFiles, vlc_executable, volume):
  setVolume(volume)
  to_play = random.sample(potentialFiles, 3) if len(potentialFiles) >= 3 else potentialFiles
  for f in to_play:
    print f

  args = [vlc_executable, "--play-and-exit", "-f", "--video-on-top"]
  args.extend(to_play)
  subprocess.Popen(args)

  if platform.system() == 'Darwin':
    subprocess.Popen("osascript -e 'tell application \"VLC\"' -e 'activate' -e 'end tell'", shell=True)



def startNightNight(directory, vlc_executable, volume, video_file_regex):
  potentialFiles = getFiles(directory, video_file_regex)
  playFiles(potentialFiles, vlc_executable, volume)


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--towatch', help="Specify which watch option you would like to watch", default="default")
parser.add_argument('-lw', '--list-watch-options', help="list all of the possible watch options", action="store_true")
args = parser.parse_args()



try:
  settingsFile = open(getSettingsFileName(), 'r')
except IOError as e:
  print "Couldn't open settings file. Are you sure it exists?"
  exit(1)

settingsString = settingsFile.read()
settings = json.loads(settingsString)
watch_options = settings['watch_options']

if args.list_watch_options:
  max_len = max(len(wo['name']) for wo in watch_options) +1
  print ("{:<" + str(max_len) + "}  {}").format("Name", "Directory")
  for watch_option in watch_options:
    print ("{:<" + str(max_len) + "}  {}").format(watch_option['name'], watch_option['directory'])
  exit(0)


towatch = None
for watch_option in watch_options:
  if watch_option['name'] == args.towatch:
    towatch = watch_option['directory']
    break

if towatch != None:
  if not os.path.exists(towatch) or not os.path.isdir(towatch):
    print "Watch option \"{0}\" has invalid directory name \"{1}\".".format(args.towatch, towatch)
    exit(1)
  else:
    vlc_executable = settings.get('vlc_executable', getVlcExecutable())
    video_file_regex = settings.get('video_file_regex', DEFAULT_VIDEO_FILE_REGEX)
    startNightNight(towatch, vlc_executable, settings["volume"], video_file_regex)
else:
  print "No watch option with the name %s." % args.towatch
  exit(1)
