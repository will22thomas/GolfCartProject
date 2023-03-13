# This example demonstrates how to use LCM with the Python select module

import select
import lcm

import camera_image_t

def my_handler(channel, data):
    msg = camera_image_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("Received from camera: \"%s\"" % msg.camera_name)
    print("Image: \"%s\"" % msg.jpeg_image)
    print("")
    print("   timestamp:     = %s" % str(msg.timestamp))
    print("   framecount     = %s" % str(msg.framecount))
    print("")

lc = lcm.LCM()
lc.subscribe("DATA", my_handler)

try:
    timeout = 1.5  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
        else:
            print("Waiting for message...")
except KeyboardInterrupt:
    pass
