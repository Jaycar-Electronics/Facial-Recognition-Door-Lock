
#set up the system, update packages, install pip and needed tools
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3-pip -y
#install python packages
sudo pip3 install opencv-python sanic asyncio numpy json

#set up the swap-size then install the face-recog package, which will compile.
sudo sed -i 's/SWAPSIZE=.*$/SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart
sudo pip3 install face-recognition

# TODO: auto-install python scripts into /usr/bin
# connect up to the init.d/ as proper
# make it behave like a proper program 

# install the doorlock program starter in /etc/init.d/
sudo cp src/doorlock.init.sh /etc/init.d/doorlock
sudo chmod +x /etc/init.d/doorlock

# this should hopefully start up the program on boot.
sudo update-rc.d doorlock defaults

# output a "helpful" message 
echo "###############################"
echo "remember: "
echo " sudo /etc/inid.d/doorlock start"
echo " sudo /etc/inid.d/doorlock stop"
echo "to start and stop the doorlock function"
echo "--"
echo "Doorlock will run from this directory, do not change this directory unless you"
echo "are able to read what these scripts are doing and change it appropriately."
echo ""
echo "    ... and remember, we're always happy for pull requests on github"
echo "https://github.com/Jaycar-Electronics/Facial-Recognition-Door-Lock"
echo "###############################"
echo " Setup done, reboot or start the command as above."
echo " Your ip is:"

ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'
