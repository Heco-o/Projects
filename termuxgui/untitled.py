import termuxgui as tg
import time
#import os

with tg.Connection() as c:
    wid = "78494ca9-cf15-485a-9db9-7f31c2ccaf30"
    # Create a remote layout
    rv = tg.RemoteViews(c)
    # Add a TextView
    tv = rv.addTextView()
    while True:
        #files = os.listdir()
        #files.sort()
        # Set the text
        rv.setText(tv, "abcdefghijklmnopqrstuvwxyz\n" * 5)
        # update the widget
        rv.updateWidget(wid)
        time.sleep(1)