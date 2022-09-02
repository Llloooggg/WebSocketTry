import json

import pyinotify

from .. import socketio

thread = None


class ModHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, evt):
        with open("data/data.json") as json_file:
            data = json.load(json_file)
        socketio.emit("file_updated", data)


def background_thread():
    handler = ModHandler()
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch("data/data.json", pyinotify.IN_CLOSE_WRITE)
    notifier.loop()


@socketio.on("connect")
def update_data():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
