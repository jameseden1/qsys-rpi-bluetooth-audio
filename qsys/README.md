# Q-SYS Script

This is a script for Q-SYS to control the Raspberry Pi.

## Control Setup:

1. Add a `Control Script` component to your design
    
    1. Set `Input Count` to 4
    
    2. Set `Output Count` to 1
    
    3. Enable the `Script Start` and `Script Stop` control pins
    
    4. Double click the component and copy-paste script.lua into it
    
    5. Edit the IP address variable to point to your Raspberry Pi

2. Add a `Custom Controls` component to your design

    1. Set Group 1 `Type` to Momentary Button
    
    2. Set Group 1 `Count` to 4

    3. Set Group 2 `Type` to Toggle Button

    4. Set Group 2 `Count` to 1

    5. Make the following connections from the buttons to the control script

        1. (Disconnect) Button 1 Output -> Script Input 1

        2. (Restart) Button 2 Output -> Script Input 2

        3. (Reboot) Button 3 Output -> Script Input 3

        4. (Script Start) Button 4 Output -> Script Start

        5. (Script Stop) Button 5 Output -> Script Stop

        6. (Enable) Button 6 Output -> Script Input 4

3. Add a `Text Controller` component to your design

    1. Connect the script output pin 1 to text controller input pin 1

4. Optionally add a Ping component

The controller is set up. Now you can place components in your design as you would like.

Turn on the Raspberry Pi and you should see the status text field update when the script is able to connect to the Pi. You can also look at the debug output of the control script.

## Audio Setup

Simply add a 2-channel AES67 Receiver and select the correct source from the dropdown
