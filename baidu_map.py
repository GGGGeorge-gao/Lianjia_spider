"""
实现目标：
    1、通过调用百度地图api和位置信息获取经纬度
    2、封装成函数被其它文件调用
"""
import json
from urllib.request import urlopen, quote


def getLocation(json_data):
    try:
        lng = json_data['result']['location']['lng']
        lat = json_data['result']['location']['lat']
        return dict(
            longitude=round(json_data['result']['location']['lng'], 7),
            latitude=round(json_data['result']['location']['lat'], 7)
        )
    except:
        print("无相关结果！")


def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'qSMQvl7N2mM2vhVwicfZmHOtffswMTMg'
    add = quote(address)  # 由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    json_data = json.loads(res)
    return getLocation(json_data)


if __name__ == '__main__':
    # 示例输出
    print(getlnglat('杭州文三西路39号'))
