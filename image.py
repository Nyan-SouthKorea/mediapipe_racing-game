# 캠, 이미지, 핸드 순으로 생성
import numpy as np
import cv2
import mediapipe as mp
import pyautogui
from config import Config

class Image():
  def __init__(self, cam_class):
    self.handle = cv2.imread('./images/handle_2.png')
    self.booster_img = cv2.resize(cv2.imread('./images/booster.png'), (Config.mark_size, Config.mark_size))
    self.drift_img = cv2.resize(cv2.imread('./images/drift.png'), (Config.mark_size, Config.mark_size))
    
    self.img_show = np.zeros((cam_class.cam_h, cam_class.cam_w, 3))
    self.img_list = {'drift_img':self.drift_img, 'booster_img':self.booster_img}
    self.logo_now = cv2.bitwise_not(np.zeros((cam_class.cam_h, cam_class.cam_w, 3), np.uint8))
    self.logo_pre = cv2.bitwise_not(np.zeros((cam_class.cam_h, cam_class.cam_w, 3), np.uint8))
    self.img_media = []


class Hand():
  def __init__(self, hand_detection_confidence, hand_tracking_confidence, image_class):
    self.screenWidth, self.screenHeight = pyautogui.size()
    self.mp_hands = mp.solutions.hands
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_drawing_styles = mp.solutions.drawing_styles
    self.hands = self.mp_hands.Hands(model_complexity = 0, min_detection_confidence=hand_detection_confidence,\
        min_tracking_confidence=hand_tracking_confidence, max_num_hands = 2)
      
    self.pos = np.where(image_class.handle < 200.0)
    self.handle_pos = list(np.where(image_class.handle < 200.0))
    self.handle_value = np.array(image_class.handle[np.where(image_class.handle < 200.0)], dtype=np.uint8)
    self.hand_busy = True


class Cam():
  def __init__(self, cam_option, video_mode, path):
    self.cam_option = cam_option
    self.video_mode = video_mode
    self.path = path
    self.cam_w, self.cam_h = Config.cam_size[cam_option][0], Config.cam_size[cam_option][1]
    self.media_w, self.media_h = Config.cam_size[cam_option][0], Config.cam_size[cam_option][1]
