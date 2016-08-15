# Introduction
Pray Times is a program give pray times, sunrise time. Build on Python & Gtk & Pyglet.
# Requirements
Python 3.5, GTK + 3.12, Pyglet, Ummalqura.

Note: Download ummalqura library from here: https://github.com/tytkal/python-hijiri-ummalqura, please not download this from pip.
# Build & Install
Just install the requirements and run PrayTimes**.py.

To install the program on fedora, apply these commands:

`sudo dnf install git gtk+  python3-pyglet python3-gobject`

`cd`

`git clone https://github.com/abdullah-radwan/Pray-Times`

`cd  ~/Pray-Times`

`sudo chmod 755 PrayTimesEn.py PrayTimesAr.py`

`git clone https://github.com/tytkal/python-hijiri-ummalqura`

`mv python-hijiri-ummalqura/umalqurra/ .`

`./PrayTimesAr.py` for arabic, `./PrayTimesEn.py` for english.

# Knows Bugs
When run the program for greater than one day, its give the pray times for the run day only. The timer solution is restart the program everyday.

After 12 AM, the program give the next pray is unknown.

When adan is started, you cannot stop it. The timer solution is close the program and open it again.

# Reference

Pray times calculation script http://praytimes.org/code/git/?a=tree&p=PrayTimes&hb=HEAD&f=v2/python. Adan http://praytimes.org/audio/. Coordinates from Islamic finder.

