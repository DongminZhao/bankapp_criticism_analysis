from util import BsUtil
import sys
import os

file = r"raw_data/MI/"
if not os.path.exists(file):
    os.makedirs(file)


def crawler_mi(app_name, app_id):
    with open(file + '/' + 'MI_' + app_name + '.txt', 'w', encoding='utf-8') as f:
        page = 0
        has_more = True
        result = BsUtil.praseJson('http://market.xiaomi.com/apm/comment/list/%s?'
                                  'clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN'
                                  '&la=zh&os=1461822601&page=%s&sdk=22' % (app_id, page))
        try:
            total = result['pointCount']
        except Exception as e:
            print(e)
            return 0
        print('xiaomi', total)

        while has_more:
            result = BsUtil.praseJson('http://market.xiaomi.com/apm/comment/list/%s?'
                                      'clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN'
                                      '&la=zh&os=1461822601&page=%s&sdk=22' % (app_id, page))

            for comment in result['comments']:
                content = comment['commentValue'].replace("\"", "'").replace(" ", "")
                # score = comment['pointValue']
                # time = comment['updateTime']
                # author = comment['nickname'].replace("\"", "'")
                try:
                    print(app_name, content)
                    try:
                        f.write(content.replace('\n', '') + '\n')
                    except Exception as e:
                        print(e)
                        pass
                except Exception as e:
                    print(sys.exc_info()[0], ":", sys.exc_info()[1])
                    print(e)
                    pass

            page += 1
            has_more = result['hasMore']


# if __name__ == '__main__':
#     crawler_mi("工商银行", 2086)
