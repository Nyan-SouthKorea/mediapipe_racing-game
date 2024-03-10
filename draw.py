import cv2
import numpy as np
import time
from event import mouse_click

def img_mix(img, logo):
    gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) # 로고파일의 색상을 그레이로 변경
    _, mask = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY) # 배경은 흰색으로, 그림을 검정색으로 변경
    mask_inv = cv2.bitwise_not(mask)
    src1_bg = cv2.bitwise_and(img,img,mask=mask) #배경에서만 연산 = src1 배경 복사
    src2_fg = cv2.bitwise_and(logo,logo, mask = mask_inv) #로고에서만 연산
    dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
    return dst

# 렉 없도록 원본 웹캠 혹은 처리된 영상만 띄운다
def draw(img_class, cam_class):
    run_click = False
    img_class.img_media = []
    if cam_class.video_mode == True:
        cap = cv2.VideoCapture(cam_class.path)
    elif cam_class.video_mode == False:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_class.cam_w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_class.cam_h)
    success, im = cap.read()
    h, w, c = im.shape
    img_class.logo_pre = cv2.bitwise_not(np.zeros((h, w, c), np.uint8))
    while cap.isOpened():
        success, img_class.img_show = cap.read()
        if not success: print("웹캠 연결 실패")
        img_class.img_show.flags.writeable = False
        img_class.img_show = cv2.cvtColor(cv2.flip(img_class.img_show, 1), cv2.COLOR_BGR2RGB) #기본 플립이랑 rgb설정
        img_class.img_media = cv2.resize(img_class.img_show, (cam_class.media_w, cam_class.media_h)) # 리사이즈 for 미디어파이프
        img_class.img_show = cv2.cvtColor(img_class.img_show, cv2.COLOR_RGB2BGR) # 출력 위해 bgr설정
        img_class.img_show = img_mix(img_class.img_show, img_class.logo_pre) # 로고랑 합치기
        cv2.imshow('Window', img_class.img_show) # 이미지 출력
        cv2.waitKey(1)
        if cam_class.video_mode == True: time.sleep(0.05)
        if run_click == False: 
            cv2.setMouseCallback('Window', mouse_click)
            run_click = True
    cap.release()