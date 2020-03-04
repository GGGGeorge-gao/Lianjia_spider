import numpy as np
from sklearn.externals import joblib
from baidu_map import getlnglat
import time

knn = joblib.load('knn.model')
# 预测示例
# result1 = knn.predict(np.array([120, 2019, 3, 2, 1, 1, 33, 1201334, 303338, 1, 1, 0, 1]).reshape(1, -1))

columns = ['房屋面积（具体到个位数）：', '年份：', '建筑类型\n||1代表塔楼\n||2代表平房\n||3代表板塔结合\n||4代表板楼',
           '装修类型\n||1代表毛坯\n||2代表简装\n||3代表精装',
           '所在区\n|| 1 代表 上城\n|| 2 代表 下城\n|| 3 代表 临安\n|| 4 代表 余杭\n|| 5 代表 富阳\n|| 6 代表 拱墅\n|| 7 代表 未知区域\n|| 8 代表 江干\n|| 9 代表 滨江\n|| 10 代表 萧山\n|| 11 代表 西湖\n|| 12 代表 钱塘新区',
           '地铁\n|| 1 代表 附近有地铁\n|| 2 代表 附近无地铁', '楼房总层数：', '具体区域（例如：西溪印象城，朝晖六区）：', '朝向（例如西南朝向 只需 输入西南即可）：']

answer = []
result = []
temp = ''
print("===========房价预测系统===========")
for i in columns:
    print('||请输入', end='')
    print(i)
    answer.append(input())

print("=========数据分析中,请稍后=========")
time.sleep(0.2)
print('...')
time.sleep(0.2)
print('...')
time.sleep(0.2)
print('...')
result.append(int(answer[0]))
result.append(int(answer[1]))
result.append(int(answer[2]) - 1)
result.append(int(answer[3]) - 1)
result.append(int(answer[4]) - 1)
result.append(int(answer[5]) - 1)
result.append(int(answer[6]))
lnglat = getlnglat('杭州' + answer[7])
lng = int(float(lnglat['longitude']) * 10000)
lat = int(float(lnglat['latitude']) * 10000)
result.append(lng)
result.append(lat)
ori = ['东', '西', '北', '南']
for j in ori:
    if j in answer[8]:
        result.append(1)
    else:
        result.append(0)

print("========分析完成========")
print("\n本次预估房价大约为：{}万元。".format(knn.predict(np.array(result).reshape(1, -1))[0]))


