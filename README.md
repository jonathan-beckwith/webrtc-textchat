# webrtc-textchat #

A very simple WebRTC text chatroom which demonstrates how to build a basic WebRTC DataChannel app.

## Description ##

Demonstrates how to set up a very simple two way text chat using WebRTC DataChannels.

This only has been tested in Chrome, may not work in Firefox or Safari.

### Usage (Python Signal Server) ###

1. Run data_switch.py (you may need to install cherrypy, use `pip install cherrypy`).
2. Navigate to [http://localhost:8003]() in two browser tabs, (or to port 8003 from another machine).
3. In one tab click host, in the other click join. `connection intiated` will be printed in the chat log, and you can now send messages directly between the two browser windows that you have open. You can close the server and still send messages between browsers.
