from handling import hand_process
from draw import draw
from image import Image, Hand, Cam
from calculator import Calculator
import threading
import cv2
import numpy as np
import time

class Drive_Start():
  def __init__(self, cam_option, video_mode, path, hand_detection_confidence, hand_tracking_confidence):
    self.cam_class = Cam(cam_option=cam_option, video_mode=video_mode, path=path)
    self.img_class = Image(cam_class=self.cam_class)
    self.hand_class = Hand(hand_detection_confidence=hand_detection_confidence, hand_tracking_confidence=hand_tracking_confidence, image_class=self.img_class)
    self.calc = Calculator()
    self.img_class.img_media = []
    self.mul_main = threading.Thread(target = draw, args=(self.img_class, self.cam_class))
    self.mul_hand = threading.Thread(target = hand_process, args=(self.img_class, self.hand_class, self.cam_class, self.calc))
  def run(self):
    time.sleep(0.001)
    self.mul_main.start()

    self.img_class.img_media = []
    while True:
      
      if len(self.img_class.img_media) > 0: break
    
    self.mul_hand.start()
    while True:
      # 빈 화면 생성
      self.img_class.logo_now = cv2.bitwise_not(np.zeros((self.cam_class.cam_h, self.cam_class.cam_w, 3), np.uint8))
      self.hand_class.hand_busy = True

      while True:
        time.sleep(0.0001)
        if self.hand_class.hand_busy == False: 
          break
      
      # logo_pre에 적용
      self.img_class.logo_pre = self.img_class.logo_now