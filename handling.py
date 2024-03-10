import cv2
import time
from config import Config
from state import State
from joystick import joystick
import numpy as np
import math

def hand_process(img_class, hand_class, cam_class, calc):
  hand_class.hand_busy = False
  while True:
      while True:
        # setting variable
        dup = []
        time.sleep(0.0001)
        if hand_class.hand_busy == True: break
        
      # img_class.logo_now[Config.mark_location['y']:Config.mark_location['y']+Config.mark_size, Config.mark_location['x']:Config.mark_location['x']+Config.mark_size] = img_class.img_list['drift_img']
      # img_class.logo_now[Config.mark_location['y']:Config.mark_location['y']+Config.mark_size, cam_class.cam_w-(Config.mark_location['x']+Config.mark_size):cam_class.cam_w-Config.mark_location['x']] = img_class.img_list['booster_img']
      results = hand_class.hands.process(img_class.img_media)
      img_class.img_show.flags.writeable = True
      results_len = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0

      if results.multi_hand_landmarks:
          if results_len == 2:
            insert_data = {}
            for i in range(2):
                classfication = results.multi_handedness[i].classification[0]
                score = classfication.score
                label = classfication.label # Left, Right
                if score < 0.8:
                    break
                if insert_data.get(label):
                    dup = -1
                    break
                insert_data[label] = results.multi_hand_landmarks[i].landmark # 21개의 list, {x:0.1, y:0.2, z:0.3}
                dup.append(label)

            else:
              calc.cf = insert_data
              State.go_state, State.new_button_state = calc.judge_hand_grab(calc.cf)  # 손 잡음 기준을 이거 하나로 보고 나머지 knn로직이랑 변수 모두 삭제!
            #   State.new_button_state = calc.judge_buttons(calc.cf, cam_class)
              left_pos, right_pos = calc.cf['Left'], calc.cf['Right']
              _, ly = left_pos[9].x, left_pos[9].y
              _, ry = right_pos[9].x, right_pos[9].y
              
              if abs(ly - ry) < 0.15:
                  State.move = 'Go'
              elif ly < ry:
                  State.move = 'Right'
              elif ly > ry:
                  State.move = 'Left'
      
      try:
        left_y, right_y = calc.cf['Left'][9].y, calc.cf['Right'][9].y
        left_x, right_x = calc.cf['Left'][9].x, calc.cf['Right'][9].x
        left_z, right_z = calc.cf['Left'][9].z, calc.cf['Right'][9].z
        
        curve_angle = -((math.atan2(right_y - left_y, right_x - left_x) * 180) / calc.PI) # 음수: 오른쪽, 양수: 왼쪽
        mul_wh = (abs(curve_angle) % 90) / 90
        
        resize_width = int(math.sqrt((right_z - left_z) ** 2 + (right_x - left_x) ** 2 + (right_y - left_y) ** 2)* (cam_class.cam_h * mul_wh + cam_class.cam_w * (1 - mul_wh)))
        
        if resize_width >= 40: # 한손에 두 손이 잡히는 경우 방지
            if abs(resize_width - calc.width) <= 10:
                pass
            elif resize_width <= calc.width:
                calc.width = min(cam_class.cam_h, cam_class.cam_w, calc.width-15)
            else:
                calc.width = min(cam_class.cam_h, cam_class.cam_w, calc.width+15)
        
        resize_handle = cv2.resize(img_class.handle, (calc.width, calc.width))
        handle_h, handle_w = resize_handle.shape[:2]
        handle_cX, handle_cY = handle_w // 2, handle_h // 2

        if curve_angle >= 0:                 
            calc.drive_angle = min(calc.drive_angle + 30, curve_angle)
        else:
            calc.drive_angle = max(calc.drive_angle - 30, curve_angle)
        
        M = cv2.getRotationMatrix2D((handle_cX, handle_cY), calc.drive_angle, 1)
        rotate_handle = cv2.warpAffine(resize_handle, M, (handle_w, handle_h), borderValue=(255, 255, 255))
        handle_pos = list(np.where((rotate_handle < 200.0)))
        handle_value = rotate_handle[np.where((rotate_handle < 200.0))]
        
        rec_cX, rec_cY = int((right_x + left_x) * cam_class.cam_w) // 2, int((right_y + left_y) * cam_class.cam_h) // 2
        handle_pos[0] += (rec_cY - handle_cY)
        handle_pos[1] += (rec_cX - handle_cX)

        indices = np.where((0 <= handle_pos[0]) & (handle_pos[0] < cam_class.cam_h) & (0 <= handle_pos[1]) & (handle_pos[1] < cam_class.cam_w))
        handle_pos[0] = handle_pos[0][indices]
        handle_pos[1] = handle_pos[1][indices]
        handle_pos[2] = handle_pos[2][indices]
        
        if State.miss_cnt >= 5 and not State.go_state:
          img_class.logo_now[handle_pos[0], handle_pos[1], handle_pos[2]] = 50
        else:
          img_class.logo_now[handle_pos[0], handle_pos[1], handle_pos[2]] = handle_value[indices]
        # cv2.putText(logo_now, text = move, org=(20, 20), fntFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 244, 255), thickness=2)
      except:
          print('Error Handle Draw', calc.cnt)
          calc.cnt += 1

      try:
        # 왼손 오른손의 랜드마크 그림
        for h_loc in ['Left', 'Right']:
            for line in Config.hand_line:
              x1 = int(calc.cf[h_loc][line[0]].x * cam_class.cam_w)
              y1 = int(calc.cf[h_loc][line[0]].y * cam_class.cam_h)
              x2 = int(calc.cf[h_loc][line[1]].x * cam_class.cam_w)
              y2 = int(calc.cf[h_loc][line[1]].y * cam_class.cam_h)
              img_class.logo_now = cv2.line(img_class.logo_now, (x1, y1), (x2, y2), (0, 255, 0), 2)
      except:
          print('Error Hand Draw', calc.cnt)
          pass
      
      joystick()

      hand_class.hand_busy = False