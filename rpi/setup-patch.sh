DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

echo 'Setup stream service'
sed -i "s|aes67path|${DIR}|g" aes67.service
sudo ln -f aes67.service /etc/systemd/system/aes67.service
sudo systemctl enable aes67.service

echo 'Setup alsaloop service'
sed -i "s|aes67path|${DIR}|g" alsaloop.service
sudo ln -f alsaloop.service /etc/systemd/system/alsaloop.service
sudo systemctl enable alsaloop.service

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
