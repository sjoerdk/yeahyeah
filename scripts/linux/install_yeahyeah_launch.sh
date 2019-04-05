#!/bin/bash
# Installation script for yeahyeah. Installs a script that launches a konsole,
# or, alternatively, focuses an already exiting yeahyeah console using xdotool

# installation locations
INSTALL_TMPDFILE=/usr/lib/tmpfiles.d/yeahyeah.conf
INSTALL_LAUNCHFILE=/usr/local/bin/yeahyeah_launch

function install_yeahyeah {
    # Make sure there is a folder for transient data (pid file is saved here)
    echo 'installing $INSTALL_TMPDFILE..'
    echo d /var/run/yeahyeah 0775 root $SUDO_USER - > /usr/lib/tmpfiles.d/yeahyeah.conf

    echo 'creating folder for transient data..'
    systemd-tmpfiles --create

    # install script itself so it can be called from any console
    echo 'Installing usr/local/bin/yeahyeah_launch'
    cp ./yeahyeah_launch /usr/local/bin/yeahyeah_launch
    chmod 751 /usr/local/bin/yeahyeah_launch

    echo "done. You can now link the command 'yeahyeah_launch' to the shortcut key of your choice"
}

echo This will install the yeahyeah launch script for user $SUDO_USER into the following locations:
echo "  $INSTALL_TMPDFILE"
echo "  $INSTALL_LAUNCHFILE"
echo ""

while true; do
    read -p "Do you wish to continue? (Yes/No)" yn
    case $yn in
        [Yy]* ) install_yeahyeah; break;;
        [Nn]* ) echo aborted; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
