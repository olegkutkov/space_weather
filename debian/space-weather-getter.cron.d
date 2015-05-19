SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/10 * * * * root /opt/space_weather/getter.py 2>&1 >> /var/log/space_weather.log
