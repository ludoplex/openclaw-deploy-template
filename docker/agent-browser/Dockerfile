# Ubuntu 24.04 with XFCE desktop and VNC for browser automation
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color

# Install XFCE, VNC, Firefox in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    xfce4 \
    xfce4-terminal \
    tigervnc-standalone-server \
    tigervnc-tools \
    dbus-x11 \
    firefox \
    curl \
    wget \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create VNC config directory
RUN mkdir -p /root/.vnc

# Set VNC password using printf method (more portable)
RUN printf '%s\n%s\n' 'OpenClaw2026' 'OpenClaw2026' | tigervncpasswd /root/.vnc/passwd

# VNC startup script
RUN echo '#!/bin/bash\nunset SESSION_MANAGER\nunset DBUS_SESSION_BUS_ADDRESS\nexec startxfce4' > /root/.vnc/xstartup \
    && chmod +x /root/.vnc/xstartup

# Startup script
RUN echo '#!/bin/bash\nvncserver :1 -geometry 1920x1080 -depth 24\ntail -f /dev/null' > /start.sh \
    && chmod +x /start.sh

EXPOSE 5901

CMD ["/start.sh"]
