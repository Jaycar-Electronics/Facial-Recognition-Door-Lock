sudo apt-get update
sudo apt-get upgrade
sudo pip3 install opencv-python sanic asyncio numpy json

sudo sed -i 's/SWAPSIZE=.*$/SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

sudo pip3 install face-recognition

sudo cp misc/doorlock.sh /etc/init.d/doorlock
sudo chmod +x /etc/init.d/doorlock

# this should hopefully start up the program on boot.
sudo update-rc.d doorlock defaults
