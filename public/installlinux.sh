#!/usr/bin/env bash
set -e

# Safety flag for non-interactive installs
export DEBIAN_FRONTEND=noninteractive

# Preseed: enable I2P service at boot automatically
echo "i2p i2p/daemon boolean true" | sudo debconf-set-selections

# Detect OS
if grep -qi "ubuntu" /etc/os-release; then
    echo "[+] Ubuntu detected – using PPA method"

    sudo apt-get update
    sudo apt-get install -y software-properties-common apt-transport-https curl

    sudo add-apt-repository -y ppa:i2p-maintainers/i2p
    sudo apt-get update
    sudo apt-get install -y i2p

else
    echo "[+] Debian detected – using official Debian repository"

    sudo apt-get update
    sudo apt-get install -y apt-transport-https lsb-release curl gnupg2

    CODENAME=$(lsb_release -sc)
    KEYRING="/usr/share/keyrings/i2p-archive-keyring.gpg"

    curl -o "$KEYRING" https://geti2p.net/_static/i2p-archive-keyring.gpg
    echo "deb [signed-by=$KEYRING] https://deb.i2p.net/ $CODENAME main" \
        | sudo tee /etc/apt/sources.list.d/i2p.list

    sudo apt-get update
    sudo apt-get install -y i2p i2p-keyring
fi

# Ensure dpkg config applied silently
sudo dpkg-reconfigure -f noninteractive i2p

echo "[+] I2P installation completed."

# Enable + start service
sudo systemctl enable i2p
sudo systemctl start i2p

echo "[+] I2P is running. Router console: http://127.0.0.1:7657"
