from playMusic import playMidi
import mido
from functools import reduce
import random
import math
import numpy as np
import os

# create second order markov chain
def markov2(midi_file, track, reducer_function):
    mid = mido.MidiFile(midi_file)
    notes = []
    for x in range(128):  # create 128*128*128 array filled with 0
        notes.append([])
        for y in range(128):
            notes[x].append([])
            for z in range(128):
                notes[x][y].append(0)

    note_ons = []
    print("Tracks:", mid.tracks)
    # TODO use note off eventually
    for i, message in enumerate(mid.tracks[track]):  # populates and isolates "note on" events
        if message.type == "note_on":
            note_ons.append(message)

    for i, message in enumerate(note_ons):  # populates 3d array frequencies
        if i < len(note_ons) - 2:
            notes[message.note][note_ons[i + 1].note][note_ons[i + 2].note] += 1

    for next_notes in notes:  # put everything through 6th root function to normalize data (communism)
        for x, next_next_notes in enumerate(next_notes):
            for y, next_next_note_prob in enumerate(next_next_notes):
                next_notes[x][y] = reducer_function(next_next_note_prob)

    for x, next_notes in enumerate(notes):  # convert note count into probabilities
        for y, next_next_notes in enumerate(next_notes):
            total = reduce((lambda a, b: a + b), next_next_notes)
            for z, next_next_note_prob in enumerate(next_next_notes):
                if total != 0 and next_next_note_prob != 0:
                    notes[x][y][z] = (next_next_note_prob / total)

    return notes
#TODO: Hardcode the markov2 function

#writes markov chain to .dat.npy
def write_to(write_to_name, midi_path, track):
    notes = markov2("midis/" + midi_path + ".mid", track, lambda x: math.pow(x, 1/4))
    filename = "frequencies/" + write_to_name + ".dat.npy"
    np.save(filename, np.array(notes))

#reads from .dat.npy, returns 3x3 frequency list
def read_from(read_from_name):
    filename = "frequencies/" + read_from_name + ".dat.npy"
    return np.load(filename).tolist()

#write_to("happy", "Bach", 1)
#write_to("sad", "Moon", 1)
#write_to("angry", "Elvis", 1)



happy = {
    'name': 'happy',
    'file': "midis/Bach.mid",
    'track': 1,
    'tempo': 250
}
happy.update({"note":read_from("happy")})

sad = {
    'name': 'sad',
    'file': "midis/Moon.mid",
    'track': 1,
    'tempo': 400
}
sad.update({"note":read_from("sad")})

angry = {
    'name': 'angry',
    'file': "midis/Elvis.mid",
    'track': 1,
    'tempo': 150
}
angry.update({"note":read_from("angry")})

disgusted = {
    'name': 'disgusted',
    'file': "midis/Bach.mid", #will end up being some low shit
    'track': 1,
    'tempo': 250
}
disgusted.update({"note":read_from("happy")})

neutral = {
    'name': 'neutral',
    'file': "midis/Bach.mid", #will end up being some normal shit
    'track': 1,
    'tempo': 250
}
neutral.update({"note":read_from("happy")})

surprised = {
    'name': 'surprised',
    'file': "midis/Bach.mid", #will end up being some spooky shit
    'track': 1,
    'tempo': 250
}
surprised.update({"note":read_from("happy")})


emotions = [happy, sad, angry, disgusted, neutral, surprised]
emotion_strings = ['happy', 'sad', 'angry', 'disgusted', 'neutral', 'surprised']


def get_emotion():
    return emotions[emotion_strings.index(str(open(os.path.expanduser("~/.emotion"), "r").read()))]


#play function
def play(markov_chain, note_duration, length, emotion_name):
    # finds two valid starting notes
    currentNote1 = random.randint(0, 127)
    currentNote2 = random.randint(0, 127)
    timeout = 0
    while reduce((lambda x, y: x + y), markov_chain[currentNote1][currentNote2]) == 0:
        currentNote1 = random.randint(0, 127)
        currentNote2 = random.randint(0, 127)
        timeout += 1
        if timeout == 10000:
            print("Empty markov chain")
            return


    for i in range(length):
        playMidi(currentNote2, note_duration / 1000, 100)
        print(currentNote2)
        temp = np.random.choice(128, 1, p=markov_chain[currentNote1][currentNote2])
        currentNote1 = currentNote2
        currentNote2 = int(temp)
        if emotion_changed():
            return


last_emotion = "happy"


def emotion_changed():
    global last_emotion
    change = False
    if last_emotion != str(open(os.path.expanduser("~/.emotion"), "r").read()):
        change = True
    last_emotion = str(open(os.path.expanduser("~/.emotion"), "r").read())
    return change


while True:
    emotion = get_emotion()
    print(emotion["name"])
    play(emotion["note"], emotion["tempo"], 1000, emotion["name"])

