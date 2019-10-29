# Facial-Recognition-Door-Lock

Want to see who's trying to enter your room? Or do you want simple key-less entry into your work shed? This project makes it easy using the raspberry pi camera and relay to door-strike to perform a simple locking mechanism.

This project provides a network web-interface so you can check up on your raspberry pi camera. Every time the raspberry pi sees a new face, it will save it onto a database and allow you to _Allow_ or _Disallow_ those people from entering your room/shed/doorway.

If it sees a face that you have _allowed_, it will activate the door-strike so you can open the door.

## Bill of Materials

We've separated the bill of materials into two parts; the core and the door-lock; if you want just the bare-bones _"do something when you see a face you recognise"_ then use the core and add your own items to it; but the instructions are written for the door-strike.

### Core

| Qty | Code                                    | Description         |
| --- | --------------------------------------- | ------------------- |
| 1   | [XC9001](http://jaycar.com.au/p/XC9001) | Raspberry Pi 3B+    |
| 1   | [XC9020](http://jaycar.com.au/p/XC9020) | Raspberry Pi Camera |

- You will need some way to power the RPI, we now have the [MP3536](https://jaycar.com.au/p/MP3536) which is specifically designed for the RPi.
- If you are activating anything such as relays or motors (other than the door-strike project), you will have to power them separately. be careful as any amount of stray power can kill the pi; When in doubt, isolate.

### Door Strike

In addition to above, the project below mentions these items:

| Qty | Code                                    | Description                  |
| --- | --------------------------------------- | ---------------------------- |
| 1   | [LA5077](http://jaycar.com.au/p/LA5077) | Narrow Fail-Safe Door Strike |
| 1   | [WC6026](http://jaycar.com.au/p/WC6026) | Cables                       |
| 1   | [XC4514](http://jaycar.com.au/p/XC4514) | Power supply module          |
| 1   | [XC4419](http://jaycar.com.au/p/XC4419) | Relay board                  |
| 1   | [PT3002](http://jaycar.com.au/p/PT3002) | 4 way Terminal block         |
| 1   | [HB6251](http://jaycar.com.au/p/HB6251) | Waterproof enclosure         |

- You will also need a 12v power supply to activate the door strike. In this project below, we are using the 12v power supply to power both the door strike and the RPi through the use of [XC4514](https://jaycar.com.au/p/XC4514)

#### Optional extras you might not have

- [XC4989](https://jaycar.com.au/p/XC4989) 16GB SD card
- [XC9030](https://jaycar.com.au/p/XC9030) NOOBS 16GB SD card
- [MP3536](https://jaycar.com.au/p/MP3536) RPi Power supply
- [XC9021](https://jaycar.com.au/p/XC9021) Raspberry Pi Night vision Camera

## Connection diagrams

The general schematic to the design is below.

![schematic](images/schematic.png)

In all, its a fairly simple set up. The RPi is provided power via the XC4514 regulator module, and drives a small relay which will shunt input power (+12v) to the door strike when needed. To control the relay, we use the RPi Camera running facial recognition code, from the `face_recognition` library by [@ageitgeu](https://github.com/ageitgey/face_recognition)


## Programming

We've set up a startup script to make it easier to install this software but it is still under a bit of development; You will be able to find more recent information regarding this project on the github page.

When you have booted into your version of linux (NOOBS, console, etc.) Type the following into a terminal:

```sh
git clone https://github.com/Jaycar-Electronics/Facial-Recognition-Door-Lock
```

once that has finished, run the setup.sh script:

```sh
cd Facial-Recognition-Door-Lock
./setup.sh
```

Leave it for a bit, it should set the program up for you then restart the raspberry pi.

While it's running, feel free to go through the [Assembly Instructions](#Assembly) and build the rest of the housing before placing the rpi in.

**Make sure to jot down the IP address through the `ifconfig` command.** There is no screen once it is all mounted, so we will have to remote into the device to make changes.

#### Technical information

The code itself is easy enough to follow and has 3 main parts:

`doorlock.py`
This is the script that pulls it all together and creates a webserver that you can issue commands to/from.

`functions.py` is the script which outlines the functions for access granted, denied, and contains the main camera/detect loop. This is the script that contains the GPIO controlling code.

`identifier.py`
This is the python object that manages the user identities, such as who is allowed in and what they look like

We've commented the code as much as possible, so check out the scripts and get a feel for what's happening if you want to modify any of the program.

The software uses `Sanic` which is a fork of the `Flask` python library, to work with asynchronous calls through the new async libraries introduced in Python3.5

Ideally, raspbian would be up to Python3.7 by now, but unfortunately, and to make the whole process a little easier to install, we're stuck on 3.5 untill raspbian update their repositories, or if someone wants to submit a "install python3.7" script that will _just work_ (tm)

Clientside is done by [Vue-Bootstrap](https://bootstrap-vue.js.org/) which makes it very easy to build dynamic displays.

## Assembly Instructions

We've tried to make this a little easier without having to buy a tonne of screws and to make it fairly waterproof, but there's always room for improvement; feel free to grab some [HP0418](https://jaycar.com.au/p/HP0418) with nuts and washers and mount the acrylic and camera(2mm size) proper.

For our purposes though, these work well:

#### Cut acrylic

The width of the HB6251 is 80mm wide, so we're aiming to cut an acrylic panel atleast 80mm wide so that it can fit snuggly into the case. Start by marking a line straight across one of the edges of the acrylic, 80mm in from the edge.

![](images/cut.jpg)

We're using our offcut in the image above but the idea is the same. We're going to be breaking the acrylic on the bench so the line needs to run from both ends of the acrylic so the cut can work properly. You can also mark another 80mm going from the edge to the first line: Once you make the first break, then you can make the second break with the line going from edge to edge.

Once the lines are marked, _score_ them with a sharp knife, by running it along the lines to make a bit of a groove. you can use the ruler to keep the knife on point, and if you're young, get an adult to help you, because safety is important.

With the groove in place, simply place the acrylic on the edge of a bench, with the bigger side on the bench, and push down on the offcut while holding the larger piece. This will break the acrylic along the groove and separate the two pieces.

![](images/push.jpg)

Repeat the process again for the second line, so you should have a small piece of acrylic atleast 80mm on one side. You can peel of the brown paper if you want to have a clear acrylic piece.

#### Prepare regulator

Solder some wires to the regulator, such that the output side has the socket connections still on them so they can plug into the RPi. The input side should have bare wires going to it, as we'll be connecting this to the stereo connector ([PT3002](https://jaycar.com.au/p/PT3002)) later.

![](images/reg.jpg)

Connect up the regulator to a power supply and a multimeter; we want to set the voltage on the regulator to a stable `5v`. The good thing about this regulator is that it is very stable and should not fail in the case of giving too much power to the RPi.

![](images/voltage.jpg)

The regulator does a great job of providing the current and stable voltage that we need.

As we are using a 3B+ model pi, it appears that the RPi does not boot properly when powered off the GPIO, as originally intended. The best method of powering the pi would be to cut and strip a spare Micro USB lead so that you can attach that to the output of the Regulator module instead of the GPIO Pins. Do some testing to see that your RPI boots up with the green light flashing through your power method before you continue to mounting.

#### Mounting

Here we just used our double-sided tape to position the regulator, relay, and camera onto the acrylic base. You could use screws and nylon washers here to make a bit more of a professional mount / display.

![](images/mount.jpg)

In the picture above, we didn't attach the camera. That will go on last once it is plugged into the RPi.

Also remember that we are using a USB plug to power the device. If the wires to your plug is a bit flimsy, you can lock them down with either zip-ties (and drill-holes near the cable) or some hot-glue to do the trick.

#### Terminal block.

The terminals are easy to place. Simply drill 4 holes in the housing to line up with each of the terminals. If you want to make the entire assembly a tad more waterproof, you can drill them underneath the unit for when you mount it to the wall, which will cover up the holes to protect from watersplashing.

![](images/terminals.png)

Remember that one Red/Black pair will be the power in, and the other will be output for the latch. You should mark this on the unit once you have mounted the terminal block (either by glue or screws) so that you do not get confused later on, otherwise the device will not turn on.

![](images/prepare.jpg)

You should put this terminal block to the side so that you have enough room in the unit for the pi to fit in, around the USB cable.

When connecting the terminals, keep in mind that there's two ways that you can connect the terminals, depending on whether you want it to be **general-case** or **active-case**. For example, if you were controlling something that ran on 5v, 48v, or something other than 12v. you would only be able to use the general case connections; as shown below.

![](images/case.png)

In the general case, you would feed power _into_ terminal `A` and when the signal is received (the correct face is identified) you would get power out on `B`.

However, for our purposes, it is easier to go with the active case, Where you simply connect the device (such as the door lock) to the `A` and `B` terminals, and power is automatically delivered at the right signal.

If you have connected relays before, this should be second nature to you.

Once that has been done, you can connect it all up and press the acrylic sheet in. You should find that the acrylic is fairly tight but not impossible fit against the walls of the container.

![](images/power.jpg)

## Use

Here is a screenshot of the device in use. Once it is hooked up to the network, find the device IP through your router settings or otherwise and open the page on a web-browser such as chrome.

![](images/screenshot.png)

Here it will generate a thumbnail of each face that it has found and has memory of, as well as the current live feed. you can delete users and deny access.

## Future improvements

There is a wide variety of what you can do with this project; for instance, if you want to connect a speaker system to it, you can use something like [PyMedia](http://pymedia.org/) to play audio such as a voice prompt to say "access denied."

the file `functions.py` has the `accessDenied` and `accessGranted` functions that define what happens when the user is denied or granted access, in our code you can see that it turns the relay on and off.

The software could also be made to run a bit faster with some more clever asynchronous/threading; we welcome pull requests through github and are always happy to discuss the code more in depth; so if you think you have what it takes, feel free to fork the project and contribute to make a better project for all.

### Beginner's changes

Changes that should be easy enough for beginners to start contributing:

- Identifier.py
  _ Set friendly names hasn't properly been implemented yet, this should just be a dictionary entry for each uid and a string being the user's real name
  _ `Merge all common names` has not been implemented
- doorlock.py
  _ `Merge all common names` commands have not been implemented
  _ Provide a way for the client to poll for new updates, showing new faces have been found.
- index/index.html
  _ Poll the server for updates
  _ Provide a better looking interface.
- functions.py
  _ Show the uid or friendly name for each person shown in the blue-square. this is done on the tutorial for facial_recognition, so it should be easy enough to copy over to this project too.
  _ Change the face_recognition library as it is too slow. dlib takes almost 1-2 seconds on each face_encoding;
