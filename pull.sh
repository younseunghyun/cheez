git pull
source /home/cheeze/cheez/bin/activate
killall -9 gunicorn
nohup gunicorn manage:app &
