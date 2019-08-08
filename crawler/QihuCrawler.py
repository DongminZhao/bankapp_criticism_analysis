from util import BsUtil
import os

file = r"raw_data/360/"
if not os.path.exists(file):
    os.makedirs(file)


def crawler_360(app_name, app_id):

    with open(file+'360_' + app_name + '.txt', 'w', encoding='utf-8') as f:
        comment_url = "http://comment.mobilem.360.cn/comment/getComments?baike=%s&start=%s&count=%s"
        start, count = 0, 50
        result = BsUtil.praseJson(comment_url % (app_id, start, 1))
        total = result['data']['total']

        print('360', total)
        while True:
            try:
                result = BsUtil.praseJson(comment_url % (app_id, start, count))
            except Exception as e:
                print(comment_url % (app_id, start, count))
                print(e)
            if not result['data']['messages']:
                break
            for comment in result['data']['messages']:
                # print(comment['username'], comment['content'], comment['score'], comment['create_time'])
                print(
                    app_name, comment['content'].replace('\n', ''), comment['create_time'])
                try:
                    f.write(comment['content'].replace('\n', '')+'\n')
                except Exception as e:
                    print(e)
                    pass

            start += 50


if __name__ == '__main__':
    crawler_360("工商银行", 48269)
