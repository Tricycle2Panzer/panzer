from aip import AipOcr
from be.model import db_conn
import sqlalchemy
import os
import cv2
import time

# 定义常量
APP_ID = '14544448'
API_KEY = 'yRZGUXAlCd0c9vQj1kAjBEfY'
SECRET_KEY = 'sc0DKGy7wZ9MeWFGZnbscbRyoDB2IQlj'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


class OCR(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def OCR_pic_cv(self):
        try:
            #获取图片
            saveDir = 'data/'
            '''
            调用电脑摄像头来自动获取图片
            '''
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
            count = 1  # 图片计数索引
            cap = cv2.VideoCapture(0)
            width, height, w = 640, 480, 360
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            crop_w_start = (width - w) // 2
            crop_h_start = (height - w) // 2
            print('width: ', width)
            print('height: ', height)

            ret, frame = cap.read()  # 获取相框
            frame = frame[crop_h_start:crop_h_start + w, crop_w_start:crop_w_start + w]  # 展示相框
            # frame=cv2.flip(frame,1,dst=None) 
            cv2.imshow("capture", frame)
            action = cv2.waitKey(1) & 0xFF
            time.sleep(3)
            cv2.imwrite("%s/%d.jpg" % (saveDir, count), cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA))
            print(u"%s: %d 张图片" % (saveDir, count))
            count += 1
            cap.release()  # 释放摄像头
            cv2.destroyAllWindows()  # 丢弃窗口

            #ocr图片获取图片文字
            path='./data/1.jpg'
            image = get_file_content(path)
            # 调用通用文字识别, 图片为本地图片
            res = client.general(image)

            print(res)

            result = []
            for item in res['words_result']:
                print(item['words'])
                result.append(item['words'])

            print(result)

        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok", result

    def OCR_pic(self, path):
        try:
            print(path)
            image = get_file_content(path)
            # 调用通用文字识别, 图片为本地图片
            res = client.general(image)
            print(res)

            result = []
            for item in res['words_result']:
                print(item['words'])
                result.append(item['words'])

            print(result)

        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok", result