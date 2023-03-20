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
subscription = lc.subscribe("DATA", my_handler)

try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass

lc.unsubscribe(subscription)
