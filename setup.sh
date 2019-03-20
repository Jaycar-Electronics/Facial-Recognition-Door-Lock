sudo apt-get update
sudo apt-get upgrade -y
sudo pip3 install opencv-python sanic asyncio numpy json

sudo sed -i 's/SWAPSIZE=.*$/SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

sudo pip3 install face-recognition

sudo cp misc/doorlock.sh /etc/init.d/doorlock
sudo chmod +x /etc/init.d/doorlock

# this should hopefully start up the program on boot.
sudo update-rc.d doorlock defaults

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
# is there a better way to do this? yes. do I care? not until I've had coffee
ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'
