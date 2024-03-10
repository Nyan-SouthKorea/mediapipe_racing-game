import math
import numpy as np
from config import Config
from state import State

class Calculator():
  def __init__(self):
    self.speed = 0
    self.drive_angle = 0
    self.PI = math.pi
    self.width = 0
    self.cf = {}
    self.cnt = 0

  def make_vector(self, p1, p2):
    v_x = p2['x'] - p1['x']
    v_y = p2['y'] - p1['y']
    v_z = p2['z'] - p1['z']
    vector = [v_x, v_y, v_z] # x, y, z축
    return vector

  # 두 벡터 사이의 각도를 구함(judge_accel에서 사용)
  def get_angle(self, vector_1, vector_2):
    # vector 형식 : [x, y, z]
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)
    innerAB = np.dot(vector_1,vector_2)
    AB = np.linalg.norm(vector_1) * np.linalg.norm(vector_2)
    angle = np.arccos(innerAB/AB)
    angle = angle / np.pi * 180
    return angle

  def judge_hand_grab(self, cf):
    hand_vector = [[9, 10],[9, 0]]
    left_pos, right_pos = cf['Left'], cf['Right']
    # 왼손
    p1 = {'x':left_pos[hand_vector[0][0]].x, 'y':left_pos[hand_vector[0][0]].y, 'z':left_pos[hand_vector[0][0]].z}
    p2 = {'x':left_pos[hand_vector[0][1]].x, 'y':left_pos[hand_vector[0][1]].y, 'z':left_pos[hand_vector[0][1]].z}
    vector_1 = self.make_vector(p1, p2)
    p1 = {'x':left_pos[hand_vector[1][0]].x, 'y':left_pos[hand_vector[1][0]].y, 'z':left_pos[hand_vector[1][0]].z}
    p2 = {'x':left_pos[hand_vector[1][1]].x, 'y':left_pos[hand_vector[1][1]].y, 'z':left_pos[hand_vector[1][1]].z}
    vector_2 = self.make_vector(p1, p2)
    angle_1 = self.get_angle(vector_1, vector_2)
    # 오른손
    p1 = {'x':right_pos[hand_vector[0][0]].x, 'y':right_pos[hand_vector[0][0]].y, 'z':right_pos[hand_vector[0][0]].z}
    p2 = {'x':right_pos[hand_vector[0][1]].x, 'y':right_pos[hand_vector[0][1]].y, 'z':right_pos[hand_vector[0][1]].z}
    vector_1 = self.make_vector(p1, p2)
    p1 = {'x':right_pos[hand_vector[1][0]].x, 'y':right_pos[hand_vector[1][0]].y, 'z':right_pos[hand_vector[1][0]].z}
    p2 = {'x':right_pos[hand_vector[1][1]].x, 'y':right_pos[hand_vector[1][1]].y, 'z':right_pos[hand_vector[1][1]].z}
    vector_2 = self.make_vector(p1, p2)
    angle_2 = self.get_angle(vector_1, vector_2)
    # 왼손 오른손 평균이 90도 이하면 잡은것으로 인정
    avr_angle = (angle_1 + angle_2) / 2
    lr_angle = sorted([angle_1, angle_2])
    print(lr_angle)
    if avr_angle > 160: return False, False
    if avr_angle < 120: return True, False
    if lr_angle[0] < 100 and lr_angle[1] > 160: return True, True
    return False, False

  def judge_buttons(self, cf, cam_class):
    # 왼, 오른 검지의 x, y변수 설정
    left_finger_x = cf['Left'][8].x * cam_class.cam_w
    left_finger_y = cf['Left'][8].y * cam_class.cam_h
    right_finger_x = cf['Right'][8].x * cam_class.cam_w
    right_finger_y = cf['Right'][8].y * cam_class.cam_h
    left_finger_xy = [left_finger_x, left_finger_y]
    right_finger_xy = [right_finger_x, right_finger_y]
    # 부스터와 드리프트 스티커 위치 설정(x1, y1, x2, y2 형식(cv2에서 네모 그릴 때 좌표 순서랑 동일))
    # drift_zone = [Config.mark_location['x'], Config.mark_location['y'], Config.mark_location['x']+Config.mark_size, Config.mark_location['y']+Config.mark_size] # 왼쪽에 드리프트 터치 존 생성
    booster_zone = [cam_class.cam_w-(Config.mark_size+Config.mark_location['x']), Config.mark_location['y'], cam_class.cam_w-Config.mark_location['x'], Config.mark_location['y']+Config.mark_size] # 오른쪽에 부스터 터치 존 생성
    # 왼, 오른 검지가 드리프트 버튼에 올라갔는지 확인
    State.new_button_state = None
    for finger_xy in [left_finger_xy, right_finger_xy]:
        # if drift_zone[0]<finger_xy[0] and finger_xy[0]<drift_zone[2] and drift_zone[1]<finger_xy[1] and finger_xy[1]<drift_zone[3]:
        #     State.new_button_state = 'drift'
        #     break
        if booster_zone[0]<finger_xy[0] and finger_xy[0]<booster_zone[2] and booster_zone[1]<finger_xy[1] and finger_xy[1]<booster_zone[3]:
            State.new_button_state = 'booster'
            break
    return State.new_button_state

