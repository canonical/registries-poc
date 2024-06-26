#!/bin/bash

ACCOUNT_ID=f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN
SIGNING_PUBLIC_KEY=xkd_Y2ay5N2Uo14v_wsCtfVJYLAVbJgxbiKM8Ne4mZBflaROriZgk2nb5i9Oebum
CHANNEL=edge


# Enable configuration registries
sudo snap set system experimental.registries=true


# Ack the assertions
echo "Acknowledging account/$ACCOUNT_ID assertion..."
snap known --remote account account-id=$ACCOUNT_ID | snap ack /dev/stdin

echo "Acknowledging account-key/$SIGNING_PUBLIC_KEY assertion..."
snap known --remote account-key public-key-sha3-384=$SIGNING_PUBLIC_KEY | snap ack /dev/stdin

echo "Acknowledging network.registry assertion..."
curl -fsSL https://raw.githubusercontent.com/canonical/registries-poc/main/network-registry.assert | snap ack /dev/stdin


# Install the snaps
install_snap() {
    echo "Installing $1..."
    sudo snap install $1 --$CHANNEL --devmode
    snap connections $1 | awk '{print $2}' | tail -n +2 | xargs -I {} sudo snap connect {}
}

install_snap aspects-poc-server
install_snap aspects-poc-control
install_snap aspects-poc-vpn
install_snap aspects-poc-reporting
