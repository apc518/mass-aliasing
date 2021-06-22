import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

class WavFormatException(Exception):
    pass
class ChannelException(Exception):
    pass

autopath = False

def find_fmt_offset(wav_bytes):
    fmt_index = 0
    for i in range(12, len(wav_bytes) - 4):
        if wav_bytes[i:i+4] == bytearray(b'fmt '):
            fmt_index = i
            break
    if fmt_index == 0:
        raise WavFormatException("Could not find \"fmt \" subchunk")
    return fmt_index - 12

def parse_sped_up(filepath, speed = 1):
    """returns the list of lists of floats which represents the wav file at filepath"""
    wav_file = open(filepath, "rb")
    wav_bytes = bytearray(wav_file.read())
    wav_file.close()
    if wav_bytes[0:4] != bytearray(b'RIFF') or wav_bytes[8:12] != bytearray(b'WAVE'):
        raise WavFormatException("Inputted file is not a valid wav file.")
    
    # because of the possibility of a JUNK chunk, we cannot assume 'fmt ' will be at index 12
    fmt_offset = find_fmt_offset(wav_bytes)
    if int.from_bytes(wav_bytes[20+fmt_offset:22+fmt_offset],'little',signed=False) != 1:
        raise WavFormatException("Invalid audio format. Must be uncompressed wav.")
    channel_num = int.from_bytes(wav_bytes[22+fmt_offset:24+fmt_offset],'little',signed=False)
    sample_rate = int.from_bytes(wav_bytes[24+fmt_offset:28+fmt_offset],'little',signed=False)
    bit_depth = int.from_bytes(wav_bytes[34+fmt_offset:36+fmt_offset],'little',signed=False)
    if bit_depth % 8 != 0:
        raise WavFormatException("Invalid bit depth. The inputted wav file has a bit depth which isn't divisible by 8.")

    data_bytes_num = int.from_bytes(wav_bytes[40+fmt_offset:44+fmt_offset],'little',signed=False)

    wav_data = wav_bytes[44+fmt_offset:44+fmt_offset+data_bytes_num]
    
    byps = int(bit_depth / 8) # bytes per sample
    audio_data = [] # a list of lists, each sublist being a channel as a list of floats
    for i in range(0,channel_num):
        audio_data.append([])

    byps_times_channel_num = byps*channel_num
    byps_tcn_times_speed = byps_times_channel_num * speed

    for k in range(0,channel_num):
        k_times_byps = k * byps
        for i in range(0, int(len(wav_data) / (byps * channel_num * speed))):
            intnum = int.from_bytes(wav_data[i*byps_tcn_times_speed + k_times_byps:i*byps_tcn_times_speed + k_times_byps + byps],'little',signed=True)
            audio_data[k].append(float(intnum / (2**(bit_depth-1) - 1)))

    return (sample_rate, audio_data)

def get_wav_bytes(audio_data, bitdepth=16, samplerate=44100):
    """returns a wav file as a bytearray based on the inputted audio_data
    the audio_data must be a list of lists of floats"""
    if type(audio_data) != list:
        raise TypeError("The argument given was not a list")
    for lst in audio_data:
        if type(lst) != list:
            raise TypeError("The argument give was not a list of lists")
        for item in lst:
            if type(item) == int:
                item = float(item)
            elif type(item) != float:
                raise TypeError("Sublists must contain floats. Found a " + str(type(item)))
            if not(item >= -1.0 and item <= 1.0):
                raise ValueError("Values must be in range [-1.0, 1.0]")
    for lst in audio_data:
        if len(lst) != len(audio_data[0]):
            raise ChannelException("Not all channels are of equal length.")

    total_samples = len(audio_data) * len(audio_data[0])
    
    start_of_file = bytearray(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00D\xac\x00\x00\x10\xb1\x02\x00\x04\x00\x10\x00data')
    slicesize = int(len(audio_data) * bitdepth / 8)
    subchunk2size = int(total_samples*bitdepth/8)
    start_of_file = start_of_file[:4] + int(36+subchunk2size).to_bytes(4,'little',signed=False) + start_of_file[8:]
    start_of_file = start_of_file[:22] + len(audio_data).to_bytes(2,'little',signed=False) + samplerate.to_bytes(4,'little',signed=False) + int(samplerate * len(audio_data) * bitdepth / 8).to_bytes(4,'little',signed=False) + slicesize.to_bytes(2,'little',signed=False) + bitdepth.to_bytes(2,'little',signed=False) + start_of_file[36:]
    start_of_file += subchunk2size.to_bytes(4,'little',signed=False)
    wav_data = bytearray()
    for i in range(0, int(total_samples / len(audio_data))):
        for k in range(0, len(audio_data)):
            smpint = int(audio_data[k][i] * (2**(bitdepth-1) - 1))
            wav_data += (smpint.to_bytes(int(bitdepth/8),'little',signed=True))
    return start_of_file + wav_data

def save(audio_data, filepath=None, bitdepth=16, samplerate=44100):
    """saves the bytes of a wav file to disk as an actual wav file"""
    wav_bytes = get_wav_bytes(audio_data, bitdepth, samplerate)

    with open(filepath, "wb") as f:
        f.write(wav_bytes)

if __name__ == "__main__":
    print("This only works with wav files ¯\_(ツ)_/¯")
    speed = ""
    while True:
        speed = input("speedup factor: ")
        try:
            speed = int(speed)
            if speed < 1:
                print("speed must be >= 1.")
                continue
            break
        except Exception:
            continue

    input("press enter to select an output file location")

    output_path = filedialog.asksaveasfilename(filetypes=[("Wave files", "*.wav")])

    if not output_path.endswith(".wav"): output_path += ".wav"

    giant_thing_of_audio = [[]]

    for f in os.listdir():
        if f.lower().endswith(("wav", "wave")):
            sample_rate, audio_data = parse_sped_up(f, speed)
            for i, item in enumerate(audio_data[0]):
                giant_thing_of_audio[0].append(item)

    save(giant_thing_of_audio, output_path)