#!/bin/bash
# Setup VNC server in the container

# Create VNC directory
mkdir -p ~/.vnc

# Set VNC password (OpenClaw2026)
echo "OpenClaw2026" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

# Create xstartup
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
EOF
chmod +x ~/.vnc/xstartup

# Start VNC server on display :1 (port 5901)
vncserver :1 -geometry 1920x1080 -depth 24

echo "VNC server started on port 5901"
echo "Password: OpenClaw2026"
