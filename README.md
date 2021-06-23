# mass-aliasing

Take a folder of wav files and speed them up with no anti-aliasing, really easily

standard library only 👍

# Usage

Run the script with `python /path/to/mass-aliasing` and the UI should be pretty straightforward. On windows it looks like this:

 ![image](https://user-images.githubusercontent.com/56745633/123074717-6965cb00-d3cc-11eb-935f-dad64a9c7bfc.png)

# Background

I made this after watching WangleLine's video on using aliasing artifacts to do cool sound design! She asks in the video if anyone knows of a faster way than rendering hours of audio in FL studio, and I figured it wouldn't be too hard to code something!

The faster you want to speed up the audio, the faster it runs. Speeding up the audio by 20 is nearly 10x faster than speeding it up by 2, and this is why its so much better than rendering the tracks in FL (or any other daw). FL studio is processing every single sample of the input audio on export, even though you're going to throw most of them out! This script only processes the samples you'll actually keep, which are a tiny fraction of the total for large speedups.
