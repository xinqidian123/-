import urllib.request
import time
from datetime import datetime
import openpyxl
from bs4 import BeautifulSoup
import json
import random

dist: dict = {"名称": "星巴克", "销量": 0, "价格": 0}
data_json = ""
urls: list = [
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=k1sbszmqlgScwdJu&cityId=982&shopName=%E6%98%9F%E5%B7%B4%E5%85%8B&power=5&mainCategoryId=132&shopType=10&_token=eJx1kF1rgzAUhv9LwDsxiaZ%2BXbrVzqK0U7sORxkarRWrNsbOfrD%2FvgjdxS4GB973POeEvJw76L0c2BghRLAMvooe2AArSNGBDAYuJgZCpmWIKcGGDOgfpmJVl0HWvz0D%2BwPPNCSrGtlNJBRgIrps6oI8LNZ3skpETTueWAGHYThxG8JxHJW8SttT1ZYK7RrID90J1phn%2FNawYxnRMV%2BeRab%2FHxRpTw%2BwLq5j1%2BfQMlWIPqW5LlmmZLnSfCY5huSQyZiiHCAyNLHIILR%2BaPrQ4bcPxDXEp7wqW%2BGK5SWOOOFsHwY826LA9f2Y3gKKCI822tofveUi7DIWvtdHnW7VhDF3u6%2Fd8cnlperXhPW0HG6oW8VXvDIj%2FlLtu2bGsmyd8As8t5qPrOTMXcdLNgvWpwtnXjpBG71W4PsHTA5%2BaA%3D%3D&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fk1sbszmqlgScwdJu&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700897042128%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%22%2BZ6Ze4sizdQmqlJ4hQYE7Z%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dlHfLikYrrEf%2FMwDCKKIlG%2BNzqQCTFojuFGaLrriuYQqgKeYLHiTp0M3%2FJfBLyquCg%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%223951ad304709ee1ca537925f7e58433a%22%7D",
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=l3WxDu61LSGHbDLU&cityId=982&shopName=%E5%BA%93%E8%BF%AA%E5%92%96%E5%95%A1&power=5&mainCategoryId=132&shopType=10&_token=eJx1kNtugkAQht9lE65K2F1OAokXKKIoNMpBrI1p5KAQEISlhdr03bsm9qIXTSb5Z76ZyT%2BZL9BaCdAwQkjELPhIW6ABzCFOBizoCO2MEFLUkSTzSFBZEP9lqiCyIGq3BtBesSQglhfEw524FNyJzCoyJY8UyweWF2ncZyw6ArKuuxINwr7vuSQ%2FVte8OnNxfYEkq6%2BwFMLBeJex7c0XkWEH9Kb%2FF9JjG2ewSD%2F7uk2gqvAQozdmJjETnVEFZqYwE5PRdUC9Lz71plo89PjQ7rd26BeoGcnPFc3S5eB7RCTNyXVIFCLHtG0%2FvjkxEokXCGu7t5Zzt44ad1eUchzy%2B6Yxw1Nh9lMzrm%2FGCg%2Br22ZQzx1Si3JQNmSRn%2BqL1ET7dYLwE9nBLUKVXxVSMp28PDfeYHV%2BgALd0stsUxr9eAy%2BfwCxUn2T&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fl3WxDu61LSGHbDLU&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700897562937%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%225tDdRGxTGqbvQL53ke%2FEdI%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dmM49GsSOPlDdbL%2FBnJce5sbTC9xK2iDJkEUykJSQM3ZdnjjCZTLHeCamVlEfaVxuA%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%2274961b1f6c1e9db08c061137188886ba%22%7D",
    "https://www.dianping.com/ajax/json/shopDynamic/promoInfo?shopId=k1x5xslgLiZ5jo1M&cityId=982&shopName=luckincoffee%E7%91%9E%E5%B9%B8%E5%92%96%E5%95%A1&power=5&mainCategoryId=132&shopType=10&_token=eJx1kG1vmzAQx7%2BLJV7NCmfABkfqizQNa1ioEkqWNlNVEZMHRjAPpiNr1e9ew7oXezHJ0v3uf3f%2Fs%2B4NNfMUjQkAOASjX%2FsGjREZwYghjFqlKy4AJy7xbAc4RuIfzSEMMNo132%2FQ%2BAehNmDLdp56JdJCrzDsMa18ImFP2HL063vmugWd2rZSY9Psum6UZomsMnkcibIw1amszJxc6EWdj4tsS3%2BWJNR%2F%2Bv%2FAPmnEycz3v7uySU3uWSY8GzPX4MTgM2NGjWtuXHtIry7ifrVtE%2BxajvYcCKyBKGYeDORixv5UPcwo6UmfiFl8IFvTMME9TMDtbfPeVsfkM7Z%2F81DfVLeq7Cg17YNLfK8cVR%2BiUO02EPqLRSxeQwGOul%2Fby0U3D75G5a6OHvIzExtrW9f%2B5pD73dRXR2ji6cs3wQMe1nehMud3B3GbHcqC1rtHWgm5LR5k8GVzrupELgOPui9yeQsgY5nTdOo%2FRutzsUqKtiwnq0k6Wden1dUVev8AWN6SJA%3D%3D&uuid=c878f49d-24f8-90de-2864-96becc427d81.1700829995&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Fk1x5xslgLiZ5jo1M&yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1700917184163%2C%22a3%22%3A%2254w5367u908055w41zwzzv252489x72281x984v0w2x97958v3y2yy9w%22%2C%22a5%22%3A%22KOPU7HH8up8bZEBcixG%2FBZ%3D%3D%22%2C%22a6%22%3A%22hs1.4RhXRbf95%2FGVxNtwgxEz6dj00ff26kDMyE8CwfA54scxNDDiU1gy%2BFyIavQ37s1Dm8Tf7eoNayBtPtR9ZdVv0Iw%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%2277a6fa44797bab1ae637524b0edd514a%22%7D",
]
Group_buying_URL: list = []


def create_urls() -> list[int]:
    global cnt
    url_s = ""
    for i in urls:
        url = i
        sleep_time = random.randint(2, 4) + random.random()
        time.sleep(sleep_time)
        ua_pool = [
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        headers = {
            "User-Agent": ua_pool[random.randint(0, len(ua_pool)-1)],
            "Cookie": "fspop=test; cy=982; cye=minhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=18c14f7ba63c8-0251b075bb2253-4c657b58-1fa400-18c14f7ba64c8; _lxsdk=18c14f7ba63c8-0251b075bb2253-4c657b58-1fa400-18c14f7ba64c8; _hc.v=61a730c4-8e5a-0ffa-39f4-7c2264540034.1701158829; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1701158830; WEBDFPID=xxxx476z7zw95uuu037u0yu83y63zy1y81x85u2w83y97958xw738665-2016518835118-1701158835118SMSOUMKfd79fef3d01d5e9aadc18ccd4d0c95071321; qruuid=6be944d9-22d6-4f7b-a28c-73ba2debc725; dper=59cbd7d042a25d7cd021476441994dea2e0146ba48d6553ce5ba7097bac2c7ca752f2e13830917efb17f7cc9b5e569f496d3a02830c1e23984a7b3724a12779e; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1701158924; JSESSIONID=24E4AD9681FABC05587F07FADDBB3C3A; _lxsdk_s=18c14f7ba64-a9a-13b-b69%7C%7C124"
        }

        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")
        # print(content)
        datas = json.loads(content)
        target_url = datas["dealMoreDetails"]
        # print(target_url)
        for j in target_url:
            Group_buying_URL.append(j["href"])
    return Group_buying_URL


def get_content(i: int, ans: list) -> str:
    sleep_time = random.randint(2,4) + random.random()
    time.sleep(sleep_time)
    url = ans[i]
    ua_pool=[
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    headers = {
        "User-Agent": ua_pool[random.randint(0,len(ua_pool)-1)],
        "Cookie":"fspop=test; cy=982; cye=minhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=18c14f7ba63c8-0251b075bb2253-4c657b58-1fa400-18c14f7ba64c8; _lxsdk=18c14f7ba63c8-0251b075bb2253-4c657b58-1fa400-18c14f7ba64c8; _hc.v=61a730c4-8e5a-0ffa-39f4-7c2264540034.1701158829; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1701158830; WEBDFPID=xxxx476z7zw95uuu037u0yu83y63zy1y81x85u2w83y97958xw738665-2016518835118-1701158835118SMSOUMKfd79fef3d01d5e9aadc18ccd4d0c95071321; qruuid=6be944d9-22d6-4f7b-a28c-73ba2debc725; dper=59cbd7d042a25d7cd021476441994dea2e0146ba48d6553ce5ba7097bac2c7ca752f2e13830917efb17f7cc9b5e569f496d3a02830c1e23984a7b3724a12779e; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1701158924; JSESSIONID=24E4AD9681FABC05587F07FADDBB3C3A; _lxsdk_s=18c14f7ba64-a9a-13b-b69%7C%7C124"
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    # print(content)
    return content


def Generate_Excel_and_jsons(i:int,content: str):
    global data_json
    soup = BeautifulSoup(content, "lxml")
    try:
        data_eval_config = soup.find("li", class_="simple-meal J_simple-meal")[
        "data-eval-config"
    ]
    except:
        content=get_content(i, Group_buying_URL)
        print("获取内容失败，正在重新尝试")
        return Generate_Excel_and_jsons(i,content)
    datas = json.loads(data_eval_config)
    data_json += data_eval_config+'\n'
    sheet.append([datas["title"], datas["price"], datas["sold"]])

if __name__ == "__main__":
    workbook = openpyxl.Workbook()
    now = datetime.now()
    sheet = workbook.active
    sheet["A1"] = "团购信息名称"
    sheet["B1"] = "团购价格"
    sheet["C1"] = "团购销售量"
    Group_buying_URL = create_urls()  # 获取星巴克、库迪、瑞幸三家所有团购信息所在页面的url
    data_json += str(now)+'\n'
    for i in range(0, len(Group_buying_URL)):
        content = get_content(i, Group_buying_URL)
        Generate_Excel_and_jsons(i,content)
        print(f"当前进度{round((i + 1) / len(Group_buying_URL),4) * 100}%")
    workbook.save("爬虫结果02.xlsx")
    with open("总的团购信息01.txt", mode="a", encoding="utf-8") as f:
        f.write(data_json)
        f.write("\n")