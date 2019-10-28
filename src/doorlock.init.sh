#!/bin/sh


### BEGIN INIT INFO
# Provides:          doorlock
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Doorlock function using rpi camera
# Description:       Doolock
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting doorlock"
    # run application you want to start

	cd /home/pi/Facial-Recognition-Door-Lock
	sudo python3 ./doorlock.py &

    ;;
  stop)
    echo "Stopping doorlock"
    # kill application you want to stop
    killall python3
    ;;
  *)
    echo "Usage: /etc/init.d/noip {start|stop}"
    exit 1
    ;;
esac

exit 0
