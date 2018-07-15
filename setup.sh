#!/usr/bin/env bash

# Check python
if ! which python3 &> /dev/null; then
    echo "Required Python3 is missing"
    exit 1
fi

# Check root
if [[ `id -u` -ne 0 ]]; then
	echo "Setup must be run as root user."
	exit 1
fi

packages=""
dpkg --list | grep build-essential &> /dev/null || packages="${packages} build-essential"
dpkg --list | grep python3-dev &> /dev/null || packages="${packages} python3-dev"
dpkg --list | grep postgresql &> /dev/null || packages="${packages} postgresql"
dpkg --list | grep postgresql-contrib &> /dev/null || packages="${packages} postgresql-contrib"
if [[ ! -z "${packages}" ]]; then
    apt-get update && apt-get install -y $packages
fi

# Check pip
if ! which pip3 &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm -f get-pip.py
else
    pip3 install pip --upgrade
fi

scriptdir=$(realpath "$(dirname $0)")
sysfile="/etc/systemd/system/recite.service"

# Check install requirements
pip3 install -r $scriptdir/requirements.txt --upgrade

if ! which uwsgi &> /dev/null; then
    echo "uWSGI is not installed"
    exit 1
fi

# Create recite service
uwsgi_cmd=`which uwsgi`
cat > $sysfile <<EOF
[Unit]
Description=uWSGI Server for recite app
After=syslog.target

[Service]
ExecStart=$uwsgi_cmd --ini $scriptdir/wsgi.ini
WorkingDirectory=$scriptdir
Restart=always
KillSignal=SIGTERM
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOF

# Create postgresql user
echo "Creating PostgreSQL user and database..."
read -p 'Username/DBname: ' psql_user
cur_dir=`pwd`
cd /var/lib/postgresql || exit
if [[ $(sudo -u postgres psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$psql_user'") -ne 1 ]]; then
    sudo -u postgres createuser -P -d $psql_user && \
    sudo -u postgres createdb $psql_user
else
    echo "User '$psql_user' was already existed, no user and database created!"
fi
cd $cur_dir || exit

# Enable and restart services
systemctl daemon-reload
systemctl restart recite.service
systemctl restart postgresql.service

echo "Done!"
