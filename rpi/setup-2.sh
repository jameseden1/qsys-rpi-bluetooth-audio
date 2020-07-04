DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# Enable loopback
echo 'Enable loopback'
sudo modprobe snd-aloop

# Set loopback to persist restarts
echo 'Make loopback persist'
echo 'snd-aloop' | sudo tee -a /etc/modules

# Redirect all audio to the loopback devices
echo 'Redirect desktop audio'
sudo ln -f asound.conf /etc/asound.conf

echo 'Setup aes67'
git clone https://github.com/bondagit/aes67-linux-daemon.git
cd aes67-linux-daemon/
sed -i '/linux-headers/d' ./ubuntu-packages.sh # remove line
sudo bash ubuntu-packages.sh
sudo bash build.sh

cd $DIR

echo 'Replace bluealsa-aplay service'
sudo ln -f bluealsa-aplay.service /etc/systemd/system/bluealsa-aplay.service

echo 'Setup stream service'
sed -i "s|aes67path|${DIR}|g" aes67.service
sudo ln -f aes67.service /etc/systemd/system/aes67.service
sudo systemctl enable aes67.service

echo 'Setup alsaloop service'
sed -i "s|aes67path|${DIR}|g" alsaloop.service
sudo ln -f alsaloop.service /etc/systemd/system/alsaloop.service
sudo systemctl enable alsaloop.service

echo 'Setup Bluetooth audio'
git clone https://github.com/nicokaiser/rpi-audio-receiver.git
cd rpi-audio-receiver
sed -i '/REPLY/d' ./install-bluetooth.sh # remove line
sudo bash install-bluetooth.sh
cd $DIR

echo 'Setup Stream Manager'
sed -i "s|aes67path|${DIR}|g" stream-manager.service
sudo ln -f stream-manager.service /etc/systemd/system/stream-manager.service
sudo systemctl enable stream-manager.service

echo 'Start everything'
sudo systemctl daemon-reload
sudo systemctl restart bluealsa-aplay
sudo systemctl restart aes67.service
sudo systemctl restart alsaloop.service
sudo systemctl restart stream-manager.service

echo 'Reboot'
sudo reboot
