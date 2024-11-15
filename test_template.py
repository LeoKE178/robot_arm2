import cv2
import numpy as np
from template_match import match_template_with_color
from pathlib import Path
from utils import match_and_wait


# frame = cv2.imread('./ACB/1.png')
# print(match_and_wait(frame,'./ACB_templates/ACB.png'))


page_path = './ACB/'
name = {
    '1': page_path+'1.png',
    '2': page_path+'2.png',
    '3': page_path+'3.png',
    '4': page_path+'4.png',
    '5': page_path+'5.png',
    '6': page_path+'6.png',
    '7': page_path+'7.png',
    '8': page_path+'8.png',
    '8_2': page_path+'8_2.png',
    '9': page_path+'9.png',
    '10': page_path+'10.png',
    '10_2': page_path+'10_2.png',
    '11_1': page_path + '11_1.png', 
    '11_2': page_path + '11_2.png', 
    '12': page_path+'12.png',
    '13': page_path + '13.png',
    '14': page_path + '14.png',
    '15': page_path + '15.png',
    '16': page_path + '16.png',
    '17': page_path + '17.png',
}

template_path = './ACB_templates/'
templates = {
    '1': template_path + 'ACB.png',
    '2_2': template_path + '2_2.png', 
    '2_1': template_path + '2_1.png', 
    '3': template_path + '3.png', 
    '4': template_path + '4.png', 
    '5': template_path + '5.png', 
    '6_1': template_path + '6_1.png', 
    '6_2': template_path + '6_2.png', 
    '7': template_path + '7.png', 
    '8': template_path + '8.png', 
    '8_2': template_path + '8.png', 
    '9': template_path + '9.png',
    '10': template_path + '10.png',
    '10_2': template_path + '10.png',  
    '11_1': template_path + '11_1.png', 
    '11_2': template_path + '11_2.png', 
    '12_1': template_path + '12_1.png',
    '12_2': template_path + '12_2.png',
    '13': template_path + '13.png',
    '14': template_path + '14.png',
    '15': template_path + '15.png',
    '16': template_path + '16.png',
    '17': template_path + '17.png',
}


result_path = Path("test_result/ACB")

name_template1 = templates['12_1']
name_template2 = templates['12_2']
template2_exist = True
template2_exist = False
# 載入圖像和模板
temp = 12
image = cv2.imread(name[f'{temp}'])
print(image.shape)
template = cv2.imread(name_template1)
print(template.shape)
if template2_exist:
    template2 = cv2.imread(name_template2)
    print(template2.shape)
# 執行模板匹配
matches = match_template_with_color(image, template)
if template2_exist:
    matches2 = match_template_with_color(image, template2)
#print(matches)
pt_x = 0
pt_y = 0
if matches != []:
    app_point = matches[0]
    app_size = template.shape
    pt_x = int(app_point[0] + app_size[1]/2)
    pt_y = int(app_point[1] + app_size[0]/2)
    print([pt_x,pt_y])
# 繪製匹配結果
if matches != []:
    cv2.rectangle(image, matches[0], (matches[0][0] + template.shape[1], matches[0][1] + template.shape[0]), (0, 255, 0), 2)
    cv2.drawMarker(image,(pt_x,pt_y), (0, 0, 255), 0)
if template2_exist:
    if matches != []:
        app_point = matches2[0]
        app_size = template2.shape
        pt_x = int(app_point[0] + app_size[1]/2)
        pt_y = int(app_point[1] + app_size[0]/2)
        print([pt_x,pt_y])
    # 繪製匹配結果
    if matches != []:
        cv2.rectangle(image, matches2[0], (matches2[0][0] + template2.shape[1], matches2[0][1] + template2.shape[0]), (0, 255, 0), 2)
        cv2.drawMarker(image,(pt_x,pt_y), (0, 0, 255), 0)
# 顯示結果
cv2.imshow('Matches', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
full_path = result_path / f'{temp}.png'

print(full_path)
cv2.imwrite(full_path,image)
