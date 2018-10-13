from playMusic import playMidi
import mido
from functools import reduce
import random
import math
import numpy as np

mid = mido.MidiFile('Bach.mid')
notes = []
for x in range(128): #create 128*128*128 array filled with 0
    notes.append([])
    for y in range(128):
        notes[x].append([])
        for z in range(128):
            notes[x][y].append(0)

print(notes[0][0][0])
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for message in track:
#         print(message)
note_ons = []

#TODO use note off eventually
for i, message in enumerate(mid.tracks[1]): #populates and isolates "note on" events
    if message.type == "note_on":
            note_ons.append(message)





for i, message in enumerate(note_ons): #populates 3d array frequencies
    if i < len(note_ons)-2:
        notes[message.note][note_ons[i + 1].note][note_ons[i + 2].note] += 1

for next_notes in notes: #put everything through 6th root function to normalize data (communism)
    for x, next_next_notes in enumerate(next_notes):
        for y, next_next_note_prob in enumerate(next_next_notes):
            next_notes[x][y] = math.pow(next_next_note_prob, 1/6)

for x, next_notes in enumerate(notes): #convert note count into probabilities
    for y, next_next_notes in enumerate(next_notes):
        total = reduce((lambda a, b: a + b), next_next_notes)
        for z, next_next_note_prob in enumerate(next_next_notes):
            if total != 0 and next_next_note_prob != 0:
                notes[x][y][z] = (next_next_note_prob / total)


#TODO: make the second note less random
#finds two valid starting notes
currentNote1 = random.randint(0,127)
currentNote2 = random.randint(0,127)
while reduce((lambda x, y: x+y), notes[currentNote1][currentNote2]) == 0:
    currentNote1 = random.randint(0,127)
    currentNote2 = random.randint(0,127)

for x in range(1000):
    playMidi(currentNote2, 150 /1000)
    print(currentNote2)
    temp = np.random.choice(128, 1, p=notes[currentNote1][currentNote2])
    currentNote1 = currentNote2
    currentNote2 = int(temp)