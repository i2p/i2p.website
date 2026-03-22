#!/usr/bin/env bash
#
# I2P Linux Easy Installer
# Detects distro and installs I2P via the appropriate package manager.
# Supports Debian, Ubuntu, Fedora, CentOS/RHEL, openSUSE, and Docker fallback.
# Offers Basic (defaults) or Advanced (bandwidth, port, UPnP) configuration.
#
# Maintained by: StormyCloud Inc.
#   admin@stormycloud.org / admin@i2p.net
# Co-maintainer: eyedeekay (idk)
#   idk@stormycloud.org
#
set -e

# Helper: set a key=value in a config file (update if exists, append if not)
set_config() {
    local key="$1" value="$2" file="$3"
    if grep -q "^${key}=" "$file" 2>/dev/null; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$file"
    else
        echo "${key}=${value}" >> "$file"
    fi
}

# ─── Collect all user input upfront ──────────────────────────────────────────

echo ""
echo "  ██╗██████╗ ██████╗"
echo "  ██║╚════██╗██╔══██╗"
echo "  ██║ █████╔╝██████╔╝"
echo "  ██║██╔═══╝ ██╔═══╝"
echo "  ██║███████╗██║"
echo "  ╚═╝╚══════╝╚═╝  Linux Installer"
echo ""
echo "  1) Basic    - Install I2P with default settings"
echo "  2) Advanced - Configure bandwidth, ports, and network"
echo ""
read -p "  Select mode [1]: " setup_mode < /dev/tty

ADVANCED=false
ADV_DL_SPEED=""
ADV_UL_SPEED=""
ADV_PORT=""
ADV_UPNP="true"

if [ "$setup_mode" = "2" ]; then
    ADVANCED=true

    # ── Speed test ───────────────────────────────────────────────────────
    echo ""
    read -p "  Run speed test to auto-configure bandwidth? [Y/n]: " run_speedtest < /dev/tty

    if [[ ! "$run_speedtest" =~ ^[Nn] ]]; then
        SPEEDTEST_TMP=$(mktemp -d)
        ARCH=$(uname -m)
        case "$ARCH" in
            x86_64)  ST_ARCH="x86_64" ;;
            aarch64) ST_ARCH="aarch64" ;;
            armv7l)  ST_ARCH="armhf" ;;
            i686)    ST_ARCH="i386" ;;
            *)       ST_ARCH="" ;;
        esac

        if [ -n "$ST_ARCH" ]; then
            ST_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-${ST_ARCH}.tgz"
            if curl -fsSL -o "$SPEEDTEST_TMP/speedtest.tgz" "$ST_URL" 2>/dev/null; then
                tar -xzf "$SPEEDTEST_TMP/speedtest.tgz" -C "$SPEEDTEST_TMP" 2>/dev/null
                echo "  Running speed test..."
                ST_OUTPUT=$("$SPEEDTEST_TMP/speedtest" --accept-license --accept-gdpr -f json 2>/dev/null || echo "")

                if [ -n "$ST_OUTPUT" ]; then
                    DL_BPS=$(echo "$ST_OUTPUT" | sed -n 's/.*"download":{[^}]*"bandwidth":\([0-9]*\).*/\1/p')
                    UL_BPS=$(echo "$ST_OUTPUT" | sed -n 's/.*"upload":{[^}]*"bandwidth":\([0-9]*\).*/\1/p')

                    if [ -n "$DL_BPS" ] && [ -n "$UL_BPS" ]; then
                        DL_KBPS=$(( DL_BPS / 1024 ))
                        UL_KBPS=$(( UL_BPS / 1024 ))
                        DL_MBPS=$(( DL_BPS * 8 / 1000000 ))
                        UL_MBPS=$(( UL_BPS * 8 / 1000000 ))
                        ADV_DL_SPEED=$(( DL_KBPS * 80 / 100 ))
                        ADV_UL_SPEED=$(( UL_KBPS * 80 / 100 ))

                        echo "  Result: ~${DL_MBPS} Mbps down / ~${UL_MBPS} Mbps up"
                        echo "  I2P will use: ${ADV_DL_SPEED} KBps in / ${ADV_UL_SPEED} KBps out (80%)"
                        echo ""
                        read -p "  Accept? [Y/n]: " accept_speed < /dev/tty
                        if [[ "$accept_speed" =~ ^[Nn] ]]; then
                            ADV_DL_SPEED=""
                            ADV_UL_SPEED=""
                        fi
                    else
                        echo "  Speed test failed to parse results."
                    fi
                else
                    echo "  Speed test failed."
                fi
            else
                echo "  Could not download speed test tool."
            fi
        else
            echo "  Speed test not available for this architecture."
        fi
        rm -rf "$SPEEDTEST_TMP"
    fi

    # Manual fallback
    if [ -z "$ADV_DL_SPEED" ] || [ -z "$ADV_UL_SPEED" ]; then
        echo ""
        echo "  Enter bandwidth (will be set to 80% of values entered)"
        read -p "  Download KBps (e.g. 12500 for ~100Mbps, blank to skip): " ADV_DL_SPEED < /dev/tty
        read -p "  Upload KBps (e.g. 6250 for ~50Mbps, blank to skip): " ADV_UL_SPEED < /dev/tty
    fi

    # ── Port ─────────────────────────────────────────────────────────────
    DEFAULT_PORT=$(( RANDOM % 21627 + 9151 ))
    echo ""
    read -p "  TCP/UDP port [${DEFAULT_PORT}]: " ADV_PORT < /dev/tty
    [ -z "$ADV_PORT" ] && ADV_PORT="$DEFAULT_PORT"

    while [ "$ADV_PORT" -lt 9151 ] || [ "$ADV_PORT" -gt 30777 ] 2>/dev/null; do
        echo "  Port must be between 9151 and 30777."
        read -p "  TCP/UDP port [${DEFAULT_PORT}]: " ADV_PORT < /dev/tty
        [ -z "$ADV_PORT" ] && ADV_PORT="$DEFAULT_PORT" && break
    done

    # ── UPnP ─────────────────────────────────────────────────────────────
    echo ""
    read -p "  Enable UPnP? [Y/n]: " upnp_answer < /dev/tty
    [[ "$upnp_answer" =~ ^[Nn] ]] && ADV_UPNP="false"

    echo ""
    echo "  Installing..."
fi

# ─── Install ────────────────────────────────────────────────────────────────

DOCKER_INSTALL=false

if grep -qiE "^ID=\"?(ubuntu|linuxmint|pop|elementary)" /etc/os-release; then
    echo "  Detected Ubuntu-based"

    export DEBIAN_FRONTEND=noninteractive
    echo "i2p i2p/daemon boolean true" | sudo debconf-set-selections 2>/dev/null

    sudo apt-get update -qq
    sudo apt-get install -y -qq software-properties-common apt-transport-https curl > /dev/null
    sudo add-apt-repository -y ppa:i2p-maintainers/i2p > /dev/null 2>&1
    sudo apt-get update -qq
    sudo apt-get install -y -qq i2p > /dev/null
    sudo dpkg-reconfigure -f noninteractive i2p 2>/dev/null

elif grep -qiE "^ID=\"?debian" /etc/os-release; then
    echo "  Detected Debian"

    export DEBIAN_FRONTEND=noninteractive
    echo "i2p i2p/daemon boolean true" | sudo debconf-set-selections 2>/dev/null

    sudo apt-get update -qq
    sudo apt-get install -y -qq apt-transport-https lsb-release curl gnupg2 > /dev/null

    CODENAME=$(lsb_release -sc)
    KEYRING="/usr/share/keyrings/i2p-archive-keyring.gpg"

    sudo curl -so "$KEYRING" https://i2p.net/i2p-archive-keyring.gpg
    echo "deb [signed-by=$KEYRING] https://deb.i2p.net/ $CODENAME main" \
        | sudo tee /etc/apt/sources.list.d/i2p.list > /dev/null

    sudo apt-get update -qq
    sudo apt-get install -y -qq i2p i2p-keyring > /dev/null
    sudo dpkg-reconfigure -f noninteractive i2p 2>/dev/null

elif grep -qiE "^ID=\"?(centos|rhel|almalinux|rocky)" /etc/os-release; then
    DISTRO_NAME=$(. /etc/os-release && echo "$NAME")
    echo "  Detected ${DISTRO_NAME}"

    EL_VER=$(. /etc/os-release && echo "${VERSION_ID%%.*}")
    EL_ARCH=$(uname -m)

    if [ "$EL_ARCH" = "x86_64" ]; then
        if [ "$EL_VER" = "9" ]; then
            COPR_CHROOT="alma+epel-9-x86_64"
        else
            COPR_CHROOT="alma+epel-${EL_VER}-x86_64_v2"
        fi
    else
        COPR_CHROOT="epel-${EL_VER}-${EL_ARCH}"
    fi

    COPR_REPO_URL="https://download.copr.fedorainfracloud.org/results/i2porg/i2p/${COPR_CHROOT}/"
    COPR_GPG_URL="https://download.copr.fedorainfracloud.org/results/i2porg/i2p/pubkey.gpg"

    sudo tee /etc/yum.repos.d/i2p-copr.repo > /dev/null << REPO
[copr:copr.fedorainfracloud.org:i2porg:i2p]
name=Copr repo for i2p owned by i2porg
baseurl=${COPR_REPO_URL}
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=${COPR_GPG_URL}
repo_gpgcheck=0
enabled=1
enabled_metadata=1
REPO

    sudo dnf install -y i2p > /dev/null

elif grep -qiE "^ID=\"?fedora" /etc/os-release; then
    echo "  Detected Fedora"

    sudo dnf copr enable -y i2porg/i2p > /dev/null 2>&1
    sudo dnf install -y i2p > /dev/null

elif grep -qiE "^ID=\"?.*opensuse" /etc/os-release; then
    if grep -qi "tumbleweed" /etc/os-release; then
        echo "  Detected openSUSE Tumbleweed"
        REPO_URL="https://download.opensuse.org/repositories/home:i2p/openSUSE_Tumbleweed/home:i2p.repo"
    else
        echo "  Detected openSUSE Leap"
        REPO_URL="https://download.opensuse.org/repositories/home:i2p/openSUSE_Leap_15.6/home:i2p.repo"
    fi

    sudo zypper addrepo -f "$REPO_URL" > /dev/null 2>&1
    sudo zypper --gpg-auto-import-keys refresh > /dev/null 2>&1
    sudo zypper install -y i2p > /dev/null

else
    echo "  Unsupported distribution."
    read -p "  Install I2P via Docker instead? [y/N]: " answer < /dev/tty

    if [[ ! "$answer" =~ ^[Yy] ]]; then
        echo "  Exiting. Visit https://geti2p.net for other options."
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        echo "  Installing Docker..."
        curl -fsSL https://get.docker.com 2>/dev/null | sh > /dev/null 2>&1
        sudo systemctl enable --now docker > /dev/null 2>&1
    fi

    echo "  Starting I2P container..."
    sudo docker pull geti2p/i2p > /dev/null
    sudo docker volume create i2p-data > /dev/null
    sudo docker run -d \
        --name i2p \
        --restart unless-stopped \
        -v i2p-data:/i2p/.i2p \
        -p 7657:7657 \
        -p 4444:4444 \
        -p 4445:4445 \
        geti2p/i2p > /dev/null

    DOCKER_INSTALL=true
fi

echo "  I2P installed."

# Fix /var/lib/i2p ownership (COPR RPM creates it as root:root but service runs as i2p)
if id i2p &>/dev/null && [ -d "/var/lib/i2p" ]; then
    sudo chown -R i2p:i2p /var/lib/i2p
fi

# ─── Apply advanced configuration ───────────────────────────────────────────

if [ "$ADVANCED" = true ] && [ "$DOCKER_INSTALL" = false ]; then

    # Detect config path
    if [ -d "/var/lib/i2p/i2p-config" ]; then
        I2P_CONFIG="/var/lib/i2p/i2p-config"
    elif [ -d "$HOME/.i2p" ]; then
        I2P_CONFIG="$HOME/.i2p"
    else
        I2P_CONFIG="/var/lib/i2p/i2p-config"
        sudo mkdir -p "$I2P_CONFIG"
    fi

    ROUTER_CONFIG="$I2P_CONFIG/router.config"

    [ ! -f "$ROUTER_CONFIG" ] && sudo touch "$ROUTER_CONFIG"

    # Bandwidth
    if [ -n "$ADV_DL_SPEED" ] && [ -n "$ADV_UL_SPEED" ]; then
        in_kbps=$(( ADV_DL_SPEED * 80 / 100 ))
        out_kbps=$(( ADV_UL_SPEED * 80 / 100 ))
        in_burst_kb=$(( in_kbps * 20 ))
        out_burst_kb=$(( out_kbps * 20 ))

        sudo bash -c "$(declare -f set_config); \
            set_config 'i2np.bandwidth.inboundKBytesPerSecond' '$in_kbps' '$ROUTER_CONFIG'; \
            set_config 'i2np.bandwidth.inboundBurstKBytesPerSecond' '$in_kbps' '$ROUTER_CONFIG'; \
            set_config 'i2np.bandwidth.inboundBurstKBytes' '$in_burst_kb' '$ROUTER_CONFIG'; \
            set_config 'i2np.bandwidth.outboundKBytesPerSecond' '$out_kbps' '$ROUTER_CONFIG'; \
            set_config 'i2np.bandwidth.outboundBurstKBytesPerSecond' '$out_kbps' '$ROUTER_CONFIG'; \
            set_config 'i2np.bandwidth.outboundBurstKBytes' '$out_burst_kb' '$ROUTER_CONFIG'"
    fi

    # Port
    if [ -n "$ADV_PORT" ]; then
        sudo bash -c "$(declare -f set_config); \
            set_config 'i2np.ntcp.port' '$ADV_PORT' '$ROUTER_CONFIG'; \
            set_config 'i2np.udp.port' '$ADV_PORT' '$ROUTER_CONFIG'; \
            set_config 'i2np.udp.internalPort' '$ADV_PORT' '$ROUTER_CONFIG'; \
            set_config 'i2np.udp.enable' 'true' '$ROUTER_CONFIG'"
    fi

    # UPnP
    sudo bash -c "$(declare -f set_config); \
        set_config 'i2np.upnp.enable' '$ADV_UPNP' '$ROUTER_CONFIG'"

    # Skip welcome wizard
    sudo bash -c "$(declare -f set_config); \
        set_config 'routerconsole.welcomeWizardComplete' 'true' '$ROUTER_CONFIG'"

    # Addressbook subscription
    SUBS_DIR="$I2P_CONFIG/addressbook"
    SUBS_FILE="$SUBS_DIR/subscriptions.txt"
    NOTBOB_URL="http://notbob.i2p/hosts.txt"

    sudo mkdir -p "$SUBS_DIR"
    [ ! -f "$SUBS_FILE" ] && sudo touch "$SUBS_FILE"
    if ! grep -qF "$NOTBOB_URL" "$SUBS_FILE" 2>/dev/null; then
        echo "$NOTBOB_URL" | sudo tee -a "$SUBS_FILE" > /dev/null
    fi

    echo "  Configuration applied."
fi

# ─── Start service ───────────────────────────────────────────────────────────

if [ "$DOCKER_INSTALL" = false ]; then
    sudo systemctl enable --now i2p > /dev/null 2>&1

    # Port forwarding reminder
    if [ -n "$ADV_PORT" ]; then
        echo "  I2P is configured to use port ${ADV_PORT}."
        echo "  While not required, forwarding your port will better integrate"
        echo "  your router into the network. Instructions: https://portforward.com"
    fi
fi

# ─── Done ────────────────────────────────────────────────────────────────────

echo ""
echo "  I2P is running. Router console: http://127.0.0.1:7657"
echo ""
