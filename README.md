# Mass Aliasing

Take a folder of wav files and speed them up with no anti-aliasing, really easily

## Setup

**For most people, you just need python!** <br/>
[Install Python](https://python.org/downloads)<br/>
If you installed python from python.org on Windows or MacOS, you already have tkinter! On Linux, you may or may not. If tkinter isn't already installed:

Linux:
```sh
sudo apt-get install python3-tk  # debian/ubuntu
sudo pacman -S tk # arch
sudo dnf install python3-tkinter # fedora
sudo yum install -y tkinter tk-devel # RedHat/CentOS/Oracle
```

Windows and MacOS should only be missing tkinter if you built python from source. <br/>
[Windows](https://tkdocs.com/tutorial/install.html#install-win-python) <br/>
[MacOS](https://tkdocs.com/tutorial/install.html#install-mac-python)

## Usage

Run the script with `python /path/to/mass-aliasing` and the UI should be pretty straightforward. On windows it looks like this:

 ![image](https://user-images.githubusercontent.com/56745633/123074717-6965cb00-d3cc-11eb-935f-dad64a9c7bfc.png)

## Background

I made this after watching [WangleLine's video on using aliasing artifacts](https://www.youtube.com/watch?v=U33ejbo3ro4) to do cool sound design! She asks in the video if anyone knows of a faster way than rendering hours of audio in FL studio, and I figured it wouldn't be too hard to code something!

The faster you want to speed up the audio, the faster it runs. Speeding up the audio by 20 is nearly 10x faster than speeding it up by 2, and this is why its so much better than rendering the tracks in FL (or any other daw). FL studio is processing every single sample of the input audio on export, even though you're going to throw most of them out! This script only processes the samples you'll actually keep, which are a tiny fraction of the total for large speedups.
