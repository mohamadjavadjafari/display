#!/usr/bin/env python
import cv2
import rospy
import message_filters
import numpy as np
from nms import non_max_suppression_fast
from imutils import resize
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from amrl_vision_common.msg import Perception, Perceptions


class Display:
    def __init__(self):
        self.bridge = CvBridge()
        self.perceptions = []

        rospy.Subscriber('/vision/perceptions', Perceptions, self.callback_per)
        rospy.Subscriber('/usb_cam/image_raw', Image, self._callback_image)

    def callback_per(self, data):
        self.perceptions = data.perceptions

    def _callback_image(self, image):
        image = self.bridge.imgmsg_to_cv2(image, "bgr8")
        height, width = image.shape[:2]
        perceptions = self.perceptions
        for perception in perceptions:
            xmin = perception.polygon.points[0].x
            ymin = perception.polygon.points[0].y
            xmax = perception.polygon.points[2].x
            ymax = perception.polygon.points[2].y
            # print(perception.name, (xmin, ymin), (xmax, ymax))
            x = int(xmin * width)
            y = int(ymin * height)
            w = int(xmax * width)
            h = int(ymax * height)
            cv2.rectangle(image, (x, y), (w, h), (0, 0, 255), 2)

        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.shutdown()

    def shutdown(self):
        cv2.destroyAllWindows()
        rospy.logwarn('shutting down...')
        rospy.signal_shutdown('close')


if __name__ == "__main__":
    rospy.init_node('display')
    display = Display()
    rospy.on_shutdown(display.shutdown)
    rospy.spin()
