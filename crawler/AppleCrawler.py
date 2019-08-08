import json
from urllib import request
import os
file = r"raw_data/Apple/"
if not os.path.exists(file):
    os.makedirs(file)


def crawler_apple(app_name, app_id):

    def get_comment(url):
        print("*"*30)
        with open(file+'Apple_' + app_name + '.txt', 'a', encoding='utf-8') as f:
            req = request.Request(url)
            req.add_header("User-Agent",
                           "iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 1 "
                           "(Build 7601)) AppleWebKit/536.27.1")
            result = request.urlopen(req, timeout=30)
            json_result = json.loads(result.read().decode())

            def result_deal():
                for comment in json_result['userReviewList']:
                    try:
                        print(app_name + comment['body'], comment['date'].replace("T", " ").replace("Z", ""))

                        try:
                            f.write(comment['body'].replace('\n', '') + '\n')
                        except Exception as e:
                            print(e)
                            print("inside")
                            pass

                    except Exception as e:
                        print(e)
                        print("outside")
                        pass

            if json_result['userReviewList']:
                result_deal()
            else:
                print('NULL')
                return 0
        return 1

    def get_data(total=300000):
        start = 0
        while total > 0:
            try:
                if total > 500:
                    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/"\
                        "userReviewsRow?cc=cn&id=%s&displayable-kind=11&startIndex=%s" \
                          "&endIndex=%s&sort=4&appVersion=all" % (
                              app_id, start, (start + 500))
                else:
                    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/"\
                        "userReviewsRow?cc=cn&id=%s&displayable-kind=11&startIndex=%s" \
                          "&endIndex=%s&sort=4&appVersion=all" % (
                              app_id, start, (start + total))
                print(url)
                total = total - 500
                start = start + 500
                if get_comment(url) == 0:
                    break

            except Exception as e:
                print(e)
                # getComment(url, game_id)
                pass

    get_data()


# if __name__ == '__main__':
#
#     crawler_apple("工商银行", 423514795)
