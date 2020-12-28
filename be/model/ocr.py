from aip import AipOcr
from be.model import db_conn
import uuid
import json
import logging
from be.model import db_conn
from be.model import error
import sqlalchemy

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

    def OCR_pic(self,path):
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

            self.conn.commit()

        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok", result