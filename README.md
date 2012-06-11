NightNight
==========

NightNight is a tiny python script to help you go to sleep :)

What It Does
============
NightNight picks three random video files from a directory and plays them for you
so that you can fall asleep to your favorite white noise.

Requirements
============
 - Python >= 2.6
 - VLC

How It Works
============
NightNight first checks your configuration file, `.night_night_settings`, which should be in your
home folder. It uses this to decide what videos to play. The settings file is in JSON format and 
a typical one looks like this:

    {
      "volume" : 2,
      "watch_options" : [
        {
          "name" : "default",
          "directory" : "/Users/kurtis/Desktop/AngryBoys"
        },
        {
          "name" : "futurama",
          "directory" : "/Users/kurtis/Desktop/Futurama"
        }
      ]
    }

By default, NightNight will play videos from the watch option with the name "default". However, if
you have more than one watch option you can choose to play it by specifying it's name with the `-w` 
or `--towatch` option. For the example settings file above, by default the folder for Angry Boys
would be used. But if we wanted to fall asleep to Futurama we would simply use the command

    python nightNight.py -w futurama

Note that your settings file should also contain a volume setting. This is the volume your computer
will be set to when you run NightNight. In addition, you can also manually
specify the path to your vlc executable by adding the "vlc_executable" attribute
to the settings file like so

    "vlc_executable" : "/path/to/executable"

Once NightNight has choosen a directory, it will recursively scan through that directory looking
for video files. When it finds all of them, it will then pick three at random and play them in 
VLC for you.

Who Are You?
============

My name is [Kurtis Nusbaum][kln].
I really like computers and programming.

License
=======
NightNight is licensed under the [GPLv2][gpl].

[kln]:https://github.com/klnusbaum/
[gpl]:https://github.com/klnusbaum/NightNight/blob/master/LICENSE
