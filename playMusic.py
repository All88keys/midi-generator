import mido,fluidsynth,time
#install msgpack as a dependency too.
fs = fluidsynth.Synth()
fs.start('coreaudio')
sfid = fs.sfload("Keys.sf2")
fs.program_select(0, sfid, 0, 0)

note_ons =[]

Main_track = mido.MidiFile('midis/Bach.mid')


fs.noteon(0, 67, 127)
time.sleep(.25)
fs.noteon(0, 76, 50)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

def playMidi(note,duration,velocity):
    fs.noteon(0,note,velocity) #velocity should change based on the genre of the music.
    time.sleep(duration)
    fs.noteoff(0,note)

# for i,tone in enumerate(Main_track.tracks[1]):
#     if tone.type == 'note_on':
#         note_ons.append(tone)
# print(note_ons)
# for i, tone in enumerate(note_ons):
#     playMidi(tone.note,.25)
# print(next_note_count)

