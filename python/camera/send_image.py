import cv2
from vimba import *
from datetime import datetime
import lcm
from camera import camera_image_t
from PIL import Image


def stream_live_data():
    msg = camera_image_t()
    # msg.camera_name = hostname
    # msg.jpeg_image = "/home/"

    # msg.timestamp = "date month year"
    # msg.framecount = 0

    lc = lcm.LCM()

    vimba = Vimba. get_instance ()
    vimba.enable_log ( LOG_CONFIG_WARNING_CONSOLE_ONLY )
    log = Log.get_instance ()
    log.critical ('Critical , visible ')
    log.error ('Error , visible ')
    log.warning ('Warning , visible ')
    log.info('Info , invisible ')
    log.trace ('Trace , invisible ')

    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Bgr8)
            cv2.imwrite('frame.jpeg', frame.as_opencv_image())

    vimba.disable_log ()

    time_part = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # msg.timestamp = time_part
    # msg.framecount += 1
    
    # publish data
    # lc.publish("DATA", msg.encode())

def test_lcm():
    msg = camera_image_t()
    msg.camera_name = "Name"
    myImage = Image.open("/home/Downloads/random-grid.jpg")
    msg.jpeg_image = myImage

    msg.timestamp = "date month year"
    msg.framecount = 0

    lc = lcm.LCM()
    lc.publish("DATA", msg.encode())



def main():
    stream_live_data()
    # test_lcm()

if __name__ == "__main__":
    main()