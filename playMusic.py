import mido,fluidsynth,time,platform #install msgpack as a dependency too.

fs = fluidsynth.Synth()

#Mac is Darwin, Linux is alsa.
if platform.system() == 'Darwin':
    fs.start('coreaudio')
else:
    fs.start('alsa')

def bootNoise():
    fs.noteon(0, 67, 127)
    time.sleep(.25)
    fs.noteon(0, 76, 100)
    time.sleep(1.0)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)

#Load
sfid = fs.sfload("soundfonts/Keys.sf2")
fs.program_select(0, sfid, 0, 0)

bootNoise()

def playMidi(note,duration,velocity):
    fs.noteon(0,note,velocity) #velocity should change based on the genre of the music.
    time.sleep(duration)
    fs.noteoff(0,note)

