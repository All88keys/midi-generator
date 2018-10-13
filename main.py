from playMusic import playMidi
import mido
from functools import reduce
import random
import math
import numpy as np

mid = mido.MidiFile('train.mid')
notes = []
for x in range(128):
    notes.append([])
    for y in range(128):
        notes[x].append(0)
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for message in track:
#         print(message)
print(notes)
note_ons = []

#TODO use note off eventually
for i, message in enumerate(mid.tracks[2]):
    if message.type == "note_on":
            note_ons.append(message)

for i, message in enumerate(note_ons):
    if i < len(note_ons)-1:
        notes[message.note][note_ons[i + 1].note] += 1

for next_notes in notes:
    for i, next_note_prob in enumerate(next_notes):
        next_notes[i] = math.pow(next_note_prob, 1/6)

for i, next_notes in enumerate(notes):
    total = reduce((lambda x, y: x + y), next_notes)
    for j, next_note_prob in enumerate(next_notes):
        if total != 0 and next_note_prob != 0:
            notes[i][j] = (next_note_prob / total)


currentNote = random.randint(0,127)
while reduce((lambda x, y: x+y), notes[currentNote]) == 0:
    currentNote = random.randint(0,127)
    print('kill me')

for x in range(1000):
    playMidi(currentNote, 150 /1000)
    print(currentNote)
    temp = np.random.choice(128, 1, p=notes[currentNote])
    currentNote = int(temp)