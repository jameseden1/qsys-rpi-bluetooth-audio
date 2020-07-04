# Q-SYS Script

This is a script for Q-SYS to control the Raspberry Pi.

Setup:

1. Add a `Control Script` component to your design
    
    1. Set `Input Count` to 3
    
    2. Set `Output Count` to 1
    
    3. Enable the `Script Start` control pin
    
    4. Double click the component and copy-paste script.lua into it
    
    5. Edit the IP address variable to point to your Raspberry Pi

2. Add a `Custom Controls` component to your design

    1. Set `Type` to Momentary Button
    
    2. Set `Count` to 4

    3. Make the following connections from the buttons to the control script

        1. (Disconnect) Button 1 Output Pin -> Script Input Pin 1

        2. (Restart) Button 2 Output Pin -> Script Input Pin 2

        3. (Reboot) Button 3 Output Pin -> Script Input Pin 4

        4. (Restart Script) Button 4 Output Pin -> Script Restart Input Pin 1

3. Add a `Text Controller` component to your design

    1. Connect the script output pin 1 to text controller input pin 1

Everything is set up. Now you can place components in your design as you would like.

Turn on the Raspberry Pi and you should see the status text field update when the script is able to connect to the Pi. You can also look at the debug output of the control script.
