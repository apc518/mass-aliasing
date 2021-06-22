# mass-aliasing

Take a folder of wav files and speed them up with no anti-aliasing, really easily

standard library only 👍

# Usage
Run the script with `python /path/to/mass-aliasing.py` in a directory with at least one wav file, then follow the prompts.

# Background
The faster you want to speed up the audio, the faster it runs. Speeding up the audio by 20 is nearly 10x faster than speeding it up by 2, and this is why its so much better than rendering the tracks in FL (or any other daw). FL studio is definitely way more optimized at what it does, but its processing every single sample of the input audio on export, even though you're going to throw most of them out! This script only processes the samples you'll actually keep, which are normally a tiny fraction of the total.
