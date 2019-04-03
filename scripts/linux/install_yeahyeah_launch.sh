# Installation script for yeahyeah. Installs a script that launches a konsole,
# or, alternatively, focuses an already exiting yeahyeah console using xdotool

echo Installing yeahyeah launch for $SUDO_USER

# Make sure there is a folder for transient data (pid file is saved here)
echo 'installing /usr/lib/tmpfiles.d/yeahyeah.conf..'
echo d /var/run/yeahyeah 0775 root $SUDO_USER - > /usr/lib/tmpfiles.d/yeahyeah.conf

echo 'creating folder for transient data..'
systemd-tmpfiles --create

# install script itself so it can be called from any console
echo 'Installing usr/local/bin/yeahyeah_launch'
cp ./yeahyeah_launch /usr/local/bin/yeahyeah_launch
chmod 751 /usr/local/bin/yeahyeah_launch

echo 'done'
