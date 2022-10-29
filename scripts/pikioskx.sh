#!/bin/sh
xset -dpms
xset s off
xset s noblank
matchbox-window-manager -use_titlebar no &
unclutter &
chromium-browser http://127.0.0.1:8080 \
   --kiosk \
   --start-fullscreen \
   --display=:0 \
   --incognito \
   --window-position=0,0 \
   --incognito \
   --noerrdialogs \
   --disable-translate \
   --no-first-run \
   --fast \
   --fast-start \
   --disable-infobars \
   --disable-features=TranslateUI \
   --disk-cache-dir=/dev/null \
   --overscroll-history-navigation=0 \
   --disable-pinch \
   --remote-debugging-port=9222 \
   --no-sandbox \
   --disable-setuid-sandbox

