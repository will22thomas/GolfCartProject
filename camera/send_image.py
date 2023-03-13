import cv2
# from vimba import *
from datetime import datetime
import lcm
import camera_image_t
from PIL import Image


def stream_live_data(hostname, port):
    msg = camera_image_t()
    msg.camera_name = hostname
    msg.jpeg_image = "/home/"

    msg.timestamp = "date month year"
    msg.framecount = 0

    lc = lcm.LCM()

    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono8)
            cv2.imwrite('frame.jpeg'), frame.as_opencv_image()

    time_part = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    msg.timestamp = time_part
    msg.framecount += 1
    
    # publish data
    lc.publish("DATA", msg.encode())

def test_lcm():
    msg = camera_image_t()
    msg.camera_name = "Name"
    myImage = Image.open("/home/Downloads/random-grid.jpg")
    myImage.show()
    msg.jpeg_image = myImage

    msg.timestamp = "date month year"
    msg.framecount = 0

    lc = lcm.LCM()
    lc.publish("DATA", msg.encode())



def main():
    # stream_live_data("169.254.228.223", 7502)
    test_lcm()

if __name__ == "__main__":
    main()