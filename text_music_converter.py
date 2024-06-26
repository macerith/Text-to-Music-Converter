from bs4 import BeautifulSoup
import requests
import time
import random
import midiutil
from midiutil import MIDIFile

input_words = input('Enter text to be converted:\n')
words = input_words.split()
base_url = 'https://www.howmanysyllables.com/syllables/'

track    = 0
channel  = 0
midi_time = 0   # In beats
duration = 1   # In beats
tempo    = 100  # In BPM
volume   = 96 # 0-127, as per the MIDI standard
rest_durations = [.25, .5, .5, 1, 1, 1, 1.5, 1.5, 2, 3]
random.seed()

pitch_dict_major = {'e': [48,48,55,52],
              't': [60,60,67,64],
              'a': [55,55,52,48],
              'i': [67,67,64,60],
              'n': [52,52,55,48],
              'o': [64,64,67,60],
              's': [50,50,52,51],
              'h': [63,63,64,63],
              'r': [53,53,55,52],
              'd': [65,65,67,64],
              'l': [58,58,56,57],
              'u': [70,70,68,69],
              'c': [57,57,56,60],
              'm': [69,69,68,72],
              'f': [59,59,58,60],
              'w': [71,71,70,72],
              'y': [56,56,57,55],
              'g': [68,68,69,67],
              'p': [51,51,52,49],
              'b': [63,63,64,61],
              'v': [54,54,55,56],
              'k': [66,66,67,68],
              'q': [47,47,46,48],
              'j': [43,43,44,46],
              'x': [49,49,50,51],
              'z': [51,51,52,53]}

pitch_dict_minor = {'e': [48,48,55,51],
              't': [60,60,67,63],
              'a': [55,55,51,48],
              'i': [67,67,63,60],
              'n': [51,51,55,48],
              'o': [63,63,67,60],
              's': [50,50,53,51],
              'h': [62,62,61,63],
              'r': [53,53,57,51],
              'd': [65,65,69,63],
              'l': [58,58,59,57],
              'u': [70,70,71,69],
              'c': [57,57,56,60],
              'm': [69,69,68,72],
              'f': [59,59,58,60],
              'w': [71,71,70,72],
              'y': [57,57,56,55],
              'g': [69,69,68,67],
              'p': [49,51,52,49],
              'b': [61,63,64,61],
              'v': [54,54,55,57],
              'k': [66,66,67,69],
              'q': [46,46,47,48],
              'j': [43,43,45,46],
              'x': [49,49,50,51],
              'z': [51,51,52,53]}

duration_dict = {1: [[1],[.5],[1],[2]],
                 2: [[.5,.5], [1,1], [.5,1], [1,.5]],
                 3: [[.25,.25,.5], [.5,.25,.25], [.25,.5,.25], [.5,.5,1]],
                 4: [[.25,.25,.25,.25], [.75,.25,.5,.5], [.5,.5,.75,.25], [.25,.75,.5,.5]],
                 5: [[.75,.25,.25,.25,.5], [.5,.25,.25,.75,.25], [.25,.25,.25,.25,.5], [.5,.5,.25,.25,.5]],
                 6: [[.5,.25,.25,.5,.25,.25], [.25,.25,.25,.25,.5,.5], [.25,.25,.5,.25,.25,.5], [.5,.5,.25,.25,.25,.25]],
                 7: [[.25,.25,.25,.25,.5,.5,1], [.5,.5,.25,.25,.5,.5,.5], [.25,.25,.5,.5,.5,.5,.5], [.5,.5,.5,.5,.25,.25,.5]],
                 8: [[.25,.25,.25,.25,.25,.25,.25,.25], [.5,.25,.25,.5,.5,.5,.25,.25], [.5,.5,.5,.5,.5,.5,.5,.5], [1,.5,.5,.25,.25,.25,.25,1]],
                 9: [[.25,.25,.25,.25,.5,.5,.5,.5,.1], [.5,.5,.5,.5,.25,.25,.25,.25,1], [1,.25,.25,.5,.25,.25,.25,.25,1], [.5,.5,.5,.25,.25,.5,.5,.5,.5]]}

dict_select = input('Major or Minor Pitch Set (0 or 1): \n')
if dict_select == '0':
    pitch_dict = pitch_dict_major
elif dict_select == '1':
    pitch_dict = pitch_dict_minor
else:
    print('Error: Invalid Pitch Dict.')
    exit()


number_input_str = input('How many tracks: \n')
number_input = int(number_input_str)
count = 0
output = MIDIFile(number_input)
for i in range(number_input):
    output.addTempo(i, midi_time, tempo)

while count < number_input:
    track = count
    midi_time = 0
    for i in range(len(words)):
        url_suffix = words[i]
        url = base_url + url_suffix
        word_no_punctuation = []
        #Accessing Syllable Website.
        website = requests.get(url)
        doc = BeautifulSoup(website.text, "html.parser")
        #Getting Syllables
        tag = doc.find(['p'], id = 'SyllableContentContainer')
        result = tag.span.string
        syllables = result.split('-')
        for l in syllables:
            #Determining note duration based on syllable length
            syllable_length = len(l)
            duration_array_large = duration_dict[syllable_length]
            duration_roll = random.randint(0,3)
            duration_array = duration_array_large[duration_roll]
            
            for x in range(syllable_length):
                duration = duration_array[x]
                pitch_array = pitch_dict.get(l[x], [48,48,48,48])
                pitch_roll = random.randint(0,3)
                pitch = pitch_array[pitch_roll]
                if l != 0 & x !=0:
                    if pitch >= (last_pitch + 12):
                        pitch = pitch - 12
                    elif pitch <= (last_pitch - 12):
                        pitch = pitch + 12
                last_pitch = pitch
                output.addNote(track, channel, pitch, midi_time, duration, volume)
                midi_time = midi_time + duration
                    
        rest = rest_durations[random.randint(0, 9)]
        midi_time = midi_time + rest
        print(f"Working on track {track + 1}...   ", round(((i/len(words))*100), 0), "%")
        time.sleep(.01)
    count += 1
    
with open("C:/Users/Tommy/Desktop/Coding/VScode Projects/Python/Text-Music Converter/output.mid", "wb") as output_file:
    output.writeFile(output_file)

print("Working...   100 %")   
print("Finished.")



