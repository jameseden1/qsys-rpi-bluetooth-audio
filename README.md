# qsys-rpi-bluetooth-audio
Bluetooth audio streaming to QSys via a Raspberry Pi

Turns a Raspberry Pi into a Bluetooth audio receiver, and sends the audio via AES67 to a Q-SYS Core.

There are two components, the Raspberry Pi audio receiver/transmitter, and the Q-SYS receiver and controller.

Essentially a wrapper around https://github.com/bondagit/aes67-linux-daemon (which is built on top of Merging Technologies ALSA RAVENNA/AES67 Driver) and https://github.com/nicokaiser/rpi-audio-receiver (which is a wrapper around BlueALSA)

