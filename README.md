# Face2Forte
They say music effects the way you feel, but what if you could have the *way you feel* effect *music* ?

Well today, ladies and gentlemen, we have done just that! Using facial recognition technology and the powers of artifical intelligence, make facial expressions at the camera to effect the tempo, pitch, and **prodecural generation** of music!

## Facial Recognition
This project uses OpenCV to detect faces and determines their emotions using the models under `models/`. Frames are streamed from a Raspberry Pi camera continuously, allowing emotions to be determined in real-time. Once an emotion is determined, it is sent to the music generator to change to that genre of music.


## Markov Chain Music

A Markov chain uses a table of probabilities to predict the next given value of a series. Using a single track (or instrument) from a midi files as input, we constructed a 3 dimensional (128x128x128) table of probabilities for what note would be played after any two given notes.

![1](https://ds055uzetaobb.cloudfront.net/image_optimizer/a844ba53e344607170c4e2ec91e35a59e681c92f.png "A Markov Chain")

Importing midi data from a wide variety of sources such as *Jailhouse Rock*, *Moonlight Symphony*, and The Minecraft Soundtrack produce drastically different procedurally generated tunes.

The midi file that we used for the neutral mood (various exerpts from The Minecraft Soundtrack) is a good way of explaining how the markov chains will work.
![2](https://raw.githubusercontent.com/TheHuskiteers/midi-generator/master/images/goodexample.png "A good example")

Starting at a random note, the markov chain picks between all the possible next notes to be played, considering the frequency that note was played next in the original midi file. In this situation, sequences of notes would be likely to gravitate towards the middle, and then go either higher or lower, creating melodies that sound familiar yet distinct.
