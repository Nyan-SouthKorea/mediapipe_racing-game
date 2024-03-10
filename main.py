from drive import Drive_Start

if __name__ == '__main__':
  drive = Drive_Start(cam_option=4, video_mode=False, path='', hand_detection_confidence=0.3, hand_tracking_confidence=0.3)
  drive.run()
