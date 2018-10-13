from playMusic import playMidi
import mido
from functools import reduce
import random
import math

print('check1')
mid = mido.MidiFile('testriver.mid')
print(mid)
#print(mid)
note_prob = []
for x in range(128):
    note_prob.append([])
    for y in range(128):
        note_prob[x].append(0)
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for message in track:
#         print(message)
print(note_prob)
note_ons = []

#TODO use note off eventually
for i, message in enumerate(mid.tracks[0]):
    if message.type == "note_on":
            note_ons.append(message)

for i, message in enumerate(note_ons):
    if i < len(note_ons)-1:
        note_prob[message.note][note_ons[i + 1].note] += 1

for problist in note_prob:
    for i, prob in enumerate(problist):
        problist[i] = math.pow(prob, 1/6)
    print(problist)

for problist in note_prob:
    for i, prob in enumerate(problist):
        if reduce((lambda x, y: x+y), problist) != 0:
            problist[i] = prob / reduce((lambda x, y: x+y), problist)



currentNote = random.randint(0,127)
while reduce((lambda x, y: x+y), note_prob[currentNote]) == 0:
    currentNote = random.randint(0,127)

for i in range(1000):
    playMidi(currentNote, 250 /1000)
    print(currentNote)
    for j, k in enumerate(note_prob[currentNote]):
        if random.randint(0,100)/100 < note_prob[currentNote][j]:
            currentNote = j



