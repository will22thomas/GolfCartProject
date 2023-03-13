import lcm

from lidar_package import item

def my_handler(channel, data):
    msg = item.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   x2 coordinate: %s" % str(msg.x2Coordinate))
    print("   y2 coordinate        = '%s'" % msg.y2Coordinate)
    print("   z2 coordinate     = %s" % str(msg.z2Coordinate))
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
