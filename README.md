# Registries PoC

A proof of concept for snap configuration sharing across snaps using snapd's configuration registries.

Please note that the previous name for _registries_ was _aspects_, that's why the snaps have the _aspects_ prefix.

## Installation

To install this PoC, simply run the installation script:

```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/canonical/registries-poc/main/install.sh)"
Acknowledging account/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN assertion...
Acknowledging account-key/xkd_Y2ay5N2Uo14v_wsCtfVJYLAVbJgxbiKM8Ne4mZBflaROriZgk2nb5i9Oebum assertion...
Acknowledging network-registry.assert assertion...
Installing aspects-poc-server...
aspects-poc-server (edge) 0.2 from Stephen Mwangi (st3v3nmw) installed
Installing aspects-poc-control...
aspects-poc-control (edge) 0.2 from Stephen Mwangi (st3v3nmw) installed
Installing aspects-poc-vpn...
aspects-poc-vpn (edge) 0.2 from Stephen Mwangi (st3v3nmw) installed
Installing aspects-poc-reporting...
aspects-poc-reporting (edge) 0.2 from Stephen Mwangi (st3v3nmw) installed
```

## Running the demo

Make sure that you've installed the PoC using the installation script above. The script should install the `server`, the `control` snap, the `vpn` snap, and the `reporting` snap.

### The control snap

Everything shouuld run automatically and the `control` snap should contact the server for registration. Once registered, the `observe-device` registry view should look like this:

```console
$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/observe-device -d
{
        "registered": 1719407517,
        "uuid": "ca155b32-2472-4650-afb0-c6f967328afe"
}
```

The `control` snap will also set the device's default configuration during its initial installation:

```console
$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-interfaces config -d
{
        "config": {
                "eth0": {
                        "interface-type": "ethernet",
                        "ip-address": "172.16.0.3"
                },
                "wlan0": {
                        "interface-type": "wifi",
                        "ip-address": "192.168.0.104"
                }
        }
}

$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-tunnel -d
{
        "interface": "eth0",
        "peers": [
                "192.168.21.3",
                "192.168.151.225",
                "192.168.21.7"
        ]
}

$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-telemetry -d
{
        "monitor-packets-received": false,
        "monitor-packets-sent": true,
        "monitor-peers": true,
        "sample-rate": 2
}

$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-device -d
{
        "server-url": "http://127.0.0.1:8000"
}
```

From then on, the `control` snap will run every minute and simulate packet flow on each of the interfaces (`config.{interface}.stats`). You can confirm this by checking the snap's daemon:

```console
$ snap logs aspects-poc-control
systemd[1]: Starting snap.aspects-poc-control.daemon.service - Service for snap application aspects-poc-control.daemon...
aspects-poc-control.daemon[409009]: eth0: 9 packets ↑, 1 packets ↓
aspects-poc-control.daemon[409009]: wlan0: 5 packets ↑, 4 packets ↓
systemd[1]: snap.aspects-poc-control.daemon.service: Deactivated successfully.
systemd[1]: Finished snap.aspects-poc-control.daemon.service - Service for snap application aspects-poc-control.daemon.
systemd[1]: Starting snap.aspects-poc-control.daemon.service - Service for snap application aspects-poc-control.daemon...
aspects-poc-control.daemon[410059]: eth0: 7 packets ↑, 4 packets ↓
aspects-poc-control.daemon[410059]: wlan0: 2 packets ↑, 4 packets ↓
systemd[1]: snap.aspects-poc-control.daemon.service: Deactivated successfully.
systemd[1]: Finished snap.aspects-poc-control.daemon.service - Service for snap application aspects-poc-control.daemon.
```

You can confirm these updates by running:

```console
$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/observe-interfaces packets-received
Key                     Value
packets-received.eth0   127
packets-received.wlan0  148

$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/observe-interfaces packets-sent
Key                 Value
packets-sent.eth0   130
packets-sent.wlan0  131
```

### The vpn snap

The `vpn` snap has a service that runs every minute to simulate changes to the VPN tunnel. This is currently limited to dropping and adding peer nodes to the opposite end of the tunnel. Each of these actions has a 10% chance of occurring.

You can confirm this by checking the snap's daemon:

```console
$ snap logs aspects-poc-vpn
systemd[1]: snap.aspects-poc-vpn.daemon.service: Deactivated successfully.
systemd[1]: Finished snap.aspects-poc-vpn.daemon.service - Service for snap application aspects-poc-vpn.daemon.
systemd[1]: Starting snap.aspects-poc-vpn.daemon.service - Service for snap application aspects-poc-vpn.daemon...
aspects-poc-vpn.daemon[412358]: No changes to tunnel.
systemd[1]: snap.aspects-poc-vpn.daemon.service: Deactivated successfully.
systemd[1]: Finished snap.aspects-poc-vpn.daemon.service - Service for snap application aspects-poc-vpn.daemon.
systemd[1]: Starting snap.aspects-poc-vpn.daemon.service - Service for snap application aspects-poc-vpn.daemon...
aspects-poc-vpn.daemon[413769]: No changes to tunnel.
systemd[1]: snap.aspects-poc-vpn.daemon.service: Deactivated successfully.
systemd[1]: Finished snap.aspects-poc-vpn.daemon.service - Service for snap application aspects-poc-vpn.daemon.
```

You can also check `observe-tunnel` registry view to see the current peers:

```console
$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/observe-tunnel peers
[
        "192.168.21.3",
        "192.168.151.225",
        "192.168.21.7"
]
```

### The reporting snap

The `reporting` snap has a service that runs every minute to collect metrics on the current state of the network. The metrics collected are controlled by the `control-metrics` registry view:

```console
$ snap get f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/network/control-telemetry -d
{
        "monitor-packets-received": false,
        "monitor-packets-sent": true,
        "monitor-peers": true,
        "sample-rate": 2
}
```

You can check the state of the network by running:

```console
$ snap logs aspects-poc-reporting -n 25
aspects-poc-reporting.daemon[389998]: INFO:root:The network stats are:
aspects-poc-reporting.daemon[389998]: INFO:root:      {'device-id': 'ca155b32-2472-4650-afb0-c6f967328afe',
aspects-poc-reporting.daemon[389998]:          'packets-sent': {'eth0': 137, 'wlan0': 141},
aspects-poc-reporting.daemon[389998]:          'tunnel-peers': ['192.168.21.3', '192.168.151.225', '192.168.21.7']}
aspects-poc-reporting.daemon[389998]: INFO:root:Next run in 30.00 seconds
aspects-poc-reporting.daemon[389998]: INFO:root:The network stats are:
aspects-poc-reporting.daemon[389998]: INFO:root:      {'device-id': 'ca155b32-2472-4650-afb0-c6f967328afe',
aspects-poc-reporting.daemon[389998]:          'packets-sent': {'eth0': 137, 'wlan0': 141},
aspects-poc-reporting.daemon[389998]:          'tunnel-peers': ['192.168.21.3', '192.168.151.225', '192.168.21.7']}
aspects-poc-reporting.daemon[389998]: INFO:root:Next run in 30.00 seconds
aspects-poc-reporting.daemon[389998]: INFO:root:The network stats are:
aspects-poc-reporting.daemon[389998]: INFO:root:      {'device-id': 'ca155b32-2472-4650-afb0-c6f967328afe',
aspects-poc-reporting.daemon[389998]:          'packets-sent': {'eth0': 138, 'wlan0': 150},
aspects-poc-reporting.daemon[389998]:          'tunnel-peers': ['192.168.21.3', '192.168.151.225', '192.168.21.7']}
aspects-poc-reporting.daemon[389998]: INFO:root:Next run in 30.00 seconds
aspects-poc-reporting.daemon[389998]: INFO:root:The network stats are:
aspects-poc-reporting.daemon[389998]: INFO:root:      {'device-id': 'ca155b32-2472-4650-afb0-c6f967328afe',
aspects-poc-reporting.daemon[389998]:          'packets-sent': {'eth0': 138, 'wlan0': 150},
aspects-poc-reporting.daemon[389998]:          'tunnel-peers': ['192.168.21.3', '192.168.151.225', '192.168.21.7']}
aspects-poc-reporting.daemon[389998]: INFO:root:Next run in 30.00 seconds
aspects-poc-reporting.daemon[389998]: INFO:root:The network stats are:
aspects-poc-reporting.daemon[389998]: INFO:root:      {'device-id': 'ca155b32-2472-4650-afb0-c6f967328afe',
aspects-poc-reporting.daemon[389998]:          'packets-sent': {'eth0': 145, 'wlan0': 154},
aspects-poc-reporting.daemon[389998]:          'tunnel-peers': ['192.168.21.3', '192.168.151.225', '192.168.21.7']}
aspects-poc-reporting.daemon[389998]: INFO:root:Next run in 30.00 seconds
```

## Server API documentation

While the server is running (corresponding snap has been installed), documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Development

Make sure you've installed the PoC using the installation script above to make sure that all assertions are acknowledged and experimental features like registries are turned on.

### Building the snaps

Run `make` or `make all` to build all snaps at once or run the following commands to build them individually:

```console
$ make control
Building control snap...
Generated snap metadata
Created snap package aspects-poc-control_0.2_amd64.snap

$ make reporting
Building reporting snap...
Generated snap metadata
Created snap package aspects-poc-reporting_0.2_amd64.snap

$ make server
Building server snap...
Generated snap metadata
Created snap package aspects-poc-server_0.2_amd64.snap

$ make vpn
Building vpn snap...
Generated snap metadata
Created snap package aspects-poc-vpn_0.2_amd64.snap
```

### Installing the snaps

To use the make targets below, make sure you have [yq](https://github.com/mikefarah/yq) installed. You can install it using [Homebrew](https://brew.sh/) or as a [snap](https://snapcraft.io/yq):

```console
$ brew install yq
$ snap install yq
```

Run `make install-all` to install all the snaps at once or run the following commands to install them individually:

```console
$ make install-server
Installing server snap...
aspects-poc-server 0.2 installed

$ make install-control
Installing control snap...
aspects-poc-control 0.2 installed

$ make install-vpn
Installing vpn snap...
aspects-poc-vpn 0.2 installed

$ make install-reporting
Installing reporting snap...
aspects-poc-reporting 0.2 installed
```
