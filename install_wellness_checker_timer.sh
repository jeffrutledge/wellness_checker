#!/bin/sh
#
# systemd
#
# This enables a timer that periodically calls the wellness checker

########### Removes Failed to init server warnings ##############
### dbus-update-activation-environment --systemd DBUS_SESSION_BUS_ADDRESS DISPLAY XAUTHORITY
#################################################################

# move to directory of script
cd "$(dirname "$0")"

# Make sure script exists
if ! [ -f ./ask_about_happiness.py ]
then
  echo "Could not find python script."
  exit 1
fi
echo "Enabling wellness checker."

# Make wellness_checker@.service from template
path_to_script=`readlink -f ./ask_about_happiness.py`
sed "s|PATH_TO_SCRIPT|$path_to_script|" wellness_checker.service.template > wellness_checker.service

# Copy and activate system daemon components
echo "Copying wellness_checker.timer and wellness_checker.service to"
echo "~/.config/systemd/user/ "
sudo cp ./wellness_checker.service ~/.config/systemd/user/
sudo cp ./wellness_checker.timer ~/.config/systemd/user/
echo "Starting and enabling wellness_checker.timer"
systemctl --user enable wellness_checker.timer
systemctl --user start wellness_checker.timer

exit 0
