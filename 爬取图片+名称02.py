import time
from bs4 import BeautifulSoup
import json
import random
import requests


ua_pool = [
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]
dist: dict = {"名称": "星巴克", "销量": 0, "价格": 0}
data_json = ""
urls: list = [
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=k1sbszmqlgScwdJu&cityId=982&shopName=%E6%98%9F%E5%B7%B4%E5%85%8B&power=5&mainCategoryId=132&shopType=10&_token=eJx1kF1rgzAUhv9LwDsxiaZ%2BXbrVzqK0U7sORxkarRWrNsbOfrD%2FvgjdxS4GB973POeEvJw76L0c2BghRLAMvooe2AArSNGBDAYuJgZCpmWIKcGGDOgfpmJVl0HWvz0D%2BwPPNCSrGtlNJBRgIrps6oI8LNZ3skpETTueWAGHYThxG8JxHJW8SttT1ZYK7RrID90J1phn%2FNawYxnRMV%2BeRab%2FHxRpTw%2BwLq5j1%2BfQMlWIPqW5LlmmZLnSfCY5huSQyZiiHCAyNLHIILR%2BaPrQ4bcPxDXEp7wqW%2BGK5SWOOOFsHwY826LA9f2Y3gKKCI822tofveUi7DIWvtdHnW7VhDF3u6%2Fd8cnlperXhPW0HG6oW8VXvDIj%2FlLtu2bGsmyd8As8t5qPrOTMXcdLNgvWpwtnXjpBG71W4PsHTA5%2BaA%3D%3D&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fk1sbszmqlgScwdJu&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700897042128%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%22%2BZ6Ze4sizdQmqlJ4hQYE7Z%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dlHfLikYrrEf%2FMwDCKKIlG%2BNzqQCTFojuFGaLrriuYQqgKeYLHiTp0M3%2FJfBLyquCg%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%223951ad304709ee1ca537925f7e58433a%22%7D",
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=l3WxDu61LSGHbDLU&cityId=982&shopName=%E5%BA%93%E8%BF%AA%E5%92%96%E5%95%A1&power=5&mainCategoryId=132&shopType=10&_token=eJx1kNtugkAQht9lE65K2F1OAokXKKIoNMpBrI1p5KAQEISlhdr03bsm9qIXTSb5Z76ZyT%2BZL9BaCdAwQkjELPhIW6ABzCFOBizoCO2MEFLUkSTzSFBZEP9lqiCyIGq3BtBesSQglhfEw524FNyJzCoyJY8UyweWF2ncZyw6ArKuuxINwr7vuSQ%2FVte8OnNxfYEkq6%2BwFMLBeJex7c0XkWEH9Kb%2FF9JjG2ewSD%2F7uk2gqvAQozdmJjETnVEFZqYwE5PRdUC9Lz71plo89PjQ7rd26BeoGcnPFc3S5eB7RCTNyXVIFCLHtG0%2FvjkxEokXCGu7t5Zzt44ad1eUchzy%2B6Yxw1Nh9lMzrm%2FGCg%2Br22ZQzx1Si3JQNmSRn%2BqL1ET7dYLwE9nBLUKVXxVSMp28PDfeYHV%2BgALd0stsUxr9eAy%2BfwCxUn2T&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fl3WxDu61LSGHbDLU&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700897562937%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%225tDdRGxTGqbvQL53ke%2FEdI%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dmM49GsSOPlDdbL%2FBnJce5sbTC9xK2iDJkEUykJSQM3ZdnjjCZTLHeCamVlEfaVxuA%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%2274961b1f6c1e9db08c061137188886ba%22%7D",
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=k1x5xslgLiZ5jo1M&cityId=982&shopName=luckincoffee%E7%91%9E%E5%B9%B8%E5%92%96%E5%95%A1&power=5&mainCategoryId=132&shopType=10&_token=eJx1kG1vmzAQx7%2BLJV7NCmfABkfqizQNa1ioEkqWNlNVEZMHRjAPpiNr1e9ew7oXezHJ0v3uf3f%2Fs%2B4NNfMUjQkAOASjX%2FsGjREZwYghjFqlKy4AJy7xbAc4RuIfzSEMMNo132%2FQ%2BAehNmDLdp56JdJCrzDsMa18ImFP2HL063vmugWd2rZSY9Psum6UZomsMnkcibIw1amszJxc6EWdj4tsS3%2BWJNR%2F%2Bv%2FAPmnEycz3v7uySU3uWSY8GzPX4MTgM2NGjWtuXHtIry7ifrVtE%2BxajvYcCKyBKGYeDORixv5UPcwo6UmfiFl8IFvTMME9TMDtbfPeVsfkM7Z%2F81DfVLeq7Cg17YNLfK8cVR%2BiUO02EPqLRSxeQwGOul%2Fby0U3D75G5a6OHvIzExtrW9f%2B5pD73dRXR2ji6cs3wQMe1nehMud3B3GbHcqC1rtHWgm5LR5k8GVzrupELgOPui9yeQsgY5nTdOo%2FRutzsUqKtiwnq0k6Wden1dUVev8AWN6SJA%3D%3D&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fk1x5xslgLiZ5jo1M&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700917184163%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%22KOPU7HH8up8bZEBcixG%2FBZ%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dj00ff26kDMyE8CwfA54scxNDDiU1gy%2BFyIavQ37s1Dm8Tf7eoNayBtPtR9ZdVv0Iw%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%2277a6fa44797bab1ae637524b0edd514a%22%7D",
]
Group_buying_URL: list = []
name = ["星巴克", "库迪", "瑞幸"]
product_name = []


def gathering(target_url, less):
    for j in less:
        Group_buying_URL.append("https://t.dianping.com/deal/" + str(j["id"]))
        product_name.append(j["productTitle"])
    for j in target_url:
        Group_buying_URL.append(j["href"])
        product_name.append(j["desc"])


def sleeping():
    sleep_time = random.randint(4, 6)
    time.sleep(sleep_time)


def create_urls() -> list[int]:  # 获取星巴克、库迪、瑞幸所有团购页面的url
    for i in range(0, 1):
        url = urls[i]
        sleeping()
        headers = {
            "User-Agent": ua_pool[random.randint(0, len(ua_pool) - 1)],
            "Cookie": "_lxsdk_cuid=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _lxsdk=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _hc.v=c878f49d-24f8-90de-2864-96becc427d81.1700829995; s_ViewType=10; WEBDFPID=54w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w-2016190024126-1700830024126QQOOOCIfd79fef3d01d5e9aadc18ccd4d0c95072559; ctu=d9fe4176131e5e7930acf6b0b64054aab1b8f995e4fcc02bccd71b8b49232af1; cy=982; cye=minhou; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1701416106,1701841996,1701851814,1701933945; qruuid=6615ccfd-1add-40b6-bf77-37be13b7cf7f; dper=6a853896a1efe19ea7b222906b698e702f489826d90dcbc4b17c04f4fdb87f641f7a716861fb1bc4a1f7b5dbd20a018a8b8f74a62910c3aea9b17a04debbfcd0; ll=7fd06e815b796be3df069dec7836c3df; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1701934344; _lxsdk_s=18c432b0cac-436-3e-444%7C%7C242",
        }
        response = requests.get(url=url, headers=headers)
        response.encoding = "utf-8"  # 访问返回的html文件
        content = response.text
        datas = json.loads(content)
        target_url = datas["dealMoreDetails"]
        target_less_url = datas["dealDetails"]
        gathering(target_url, target_less_url)
        print(name[i] + "已就绪")
    return Group_buying_URL


def get_content(index: int, ans: list):
    url = ans[index]
    headers = {
        "User-Agent": ua_pool[random.randint(0, len(ua_pool) - 1)],
        "Cookie": "_lxsdk_cuid=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _lxsdk=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _hc.v=c878f49d-24f8-90de-2864-96becc427d81.1700829995; s_ViewType=10; WEBDFPID=54w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w-2016190024126-1700830024126QQOOOCIfd79fef3d01d5e9aadc18ccd4d0c95072559; ctu=d9fe4176131e5e7930acf6b0b64054aab1b8f995e4fcc02bccd71b8b49232af1; cy=982; cye=minhou; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1701416106,1701841996,1701851814,1701933945; qruuid=6615ccfd-1add-40b6-bf77-37be13b7cf7f; dper=6a853896a1efe19ea7b222906b698e702f489826d90dcbc4b17c04f4fdb87f641f7a716861fb1bc4a1f7b5dbd20a018a8b8f74a62910c3aea9b17a04debbfcd0; ll=7fd06e815b796be3df069dec7836c3df; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1701934344; _lxsdk_s=18c432b0cac-436-3e-444%7C%7C242",
    }
    sleeping()
    try:
        response = requests.get(url=url, headers=headers)
    except:
        return get_content(index, ans)
    response.encoding = "utf-8"
    content = response.text
    global data_json
    soup = BeautifulSoup(content, "lxml")
    data_eval_config = soup.find("li", class_="simple-meal J_simple-meal")[
        "data-eval-config"
    ]
    data_json += data_eval_config + "\n"
    img_src = soup.find("div", class_="img-wrap J_wrap")
    img_url = img_src.contents[1].attrs["lazy-src-load"]
    print(img_url)
    return img_url


def generate_imgs(content, index: int):  #
    headers = {
        "User-Agent": ua_pool[random.randint(0, len(ua_pool) - 1)],
        "Cookie": "_lxsdk_cuid=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _lxsdk=18c015e1ff3c8-02cec7c051cf14-6b325057-144000-18c015e1ff3c8; _hc.v=c878f49d-24f8-90de-2864-96becc427d81.1700829995; s_ViewType=10; WEBDFPID=54w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w-2016190024126-1700830024126QQOOOCIfd79fef3d01d5e9aadc18ccd4d0c95072559; ctu=d9fe4176131e5e7930acf6b0b64054aab1b8f995e4fcc02bccd71b8b49232af1; cy=982; cye=minhou; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1701416106,1701841996,1701851814,1701933945; qruuid=6615ccfd-1add-40b6-bf77-37be13b7cf7f; dper=6a853896a1efe19ea7b222906b698e702f489826d90dcbc4b17c04f4fdb87f641f7a716861fb1bc4a1f7b5dbd20a018a8b8f74a62910c3aea9b17a04debbfcd0; ll=7fd06e815b796be3df069dec7836c3df; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1701934344; _lxsdk_s=18c432b0cac-436-3e-444%7C%7C242",
    }
    sleeping()
    try:
        res = requests.get(url=content, headers=headers)
        with open(product_name[index] + ".png", "wb") as f:
            f.write(res.content)
    except:
        generate_imgs(content, index)


if __name__ == "__main__":
    Group_buying_URL = create_urls()
    for i in range(0, 5):
        content = get_content(i, Group_buying_URL)
        generate_imgs(content, i)
        print(
            f"当前进度{round(100 * (i + 1) / len(Group_buying_URL), 2)}%,还剩{len(Group_buying_URL) - i - 1}个"
        )
    with open("总的团购信息01.txt", mode="a", encoding="utf-8") as f:
        f.write(data_json)
        f.write("\n")