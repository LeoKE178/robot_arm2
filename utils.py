import requests
import cv2
import time
from coordinates import coordinates
import json
from template_match import match_template_with_color

coords = coordinates()
def load_config():
    # 从 JSON 文件加载配置
    with open('hco.json', 'r') as json_file:
        hco = json.load(json_file)
    return hco 

def move(pos):
    url0 = "http://127.0.0.1:8082/MyWcfService/getstring?duankou=0&"
    id = load_config()
    hco = f'hco={id[1:-1]}&'
    location =  f'daima=X{pos[0]}Y{pos[1]}Z{pos[2]}'
    url = url0+hco+location
    response = requests.get(url)
    time.sleep(0.05)

def push(pos):
    pos[2] = pos[2]+6
    move(pos)
    return pos

def lift(pos):
    pos[2] = pos[2]-6
    move(pos)
    return pos

def click(pos):
    time.sleep(0.1)
    pos = push(pos)
    time.sleep(0.1)
    pos = lift(pos)


def slide(pos,pos2):
    pos = push(pos)
    #print(f'what the pos{pos}')
    time.sleep(0.2)
    x_distance = pos2[0]-pos[0]
    y_distance = pos2[1]-pos[1]
    for i in range(3):
        pos[0] = pos[0]+int(x_distance/3)
        pos[1] = pos[1]+int(y_distance/3)
        #print(f'what the pos{pos}')
        move(pos)
    pos = lift(pos)
    #print(f'what the {pos}')
    return pos

def stand_by():
    pos = [90, -90, 0]
    move(pos)
    time.sleep(1)
    return pos

def unlock_screen():
    pos = [20,-20,0]
    move(pos)
    time.sleep(0.5)
    click(pos)
    click(pos)
    time.sleep(1)
    #print(f'what the {pos}')
    pos = slide(pos,[pos[0],pos[1]-60,pos[2]])
    time.sleep(1)
    lock = '112233'
    for x in lock:
        if x in coords.lock:
            pos2 = coords.get_lock(x)
            if not (pos[0] == pos2[0] and pos[1] == pos2[1]):
                pos[0] = pos2[0]
                pos[1] = pos2[1]
                move(pos)
                time.sleep(0.5)
            click(pos)
            time.sleep(0.2)
            print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')
        else:
            print('illegal lock number')
    time.sleep(1)
    return stand_by()

def close_app():
    pos = [12,-1,0]
    move(pos)
    time.sleep(0.5)
    click(pos)
    time.sleep(0.2)
    pos = [32,-30,0]
    move(pos)
    time.sleep(0.5)
    click(pos)
    time.sleep(0.2)
    pos = [33,-1,0]
    move(pos)
    time.sleep(0.5)
    click(pos)

def pos_transform(pos):
    x = pos[0]
    y = pos[1]
    pos[0] = 0.25*x
    pos[1] = 0.25*y-147
    return pos

def match_and_click(img, template_path, pos, wait_time=0.2):
    """通用图像匹配并点击"""
    template = cv2.imread(template_path)
    match_result = match_template_with_color(img, template)
    
    
    if match_result:
        # 提取匹配点并缩放
        pt = match_result[0]
        app_size = template.shape
        pt_x = int((pt[0] + app_size[1]/2 ))
        pt_y = int((pt[1] + app_size[0]/2 ))
        pos[0] = pt_x
        pos[1] = pt_y
        pos = pos_transform(pos)
        move(pos)
        time.sleep(0.5)
        click(pos)
        time.sleep(wait_time)
        return True
    return False


def match_and_wait(img, template_path, wait_time=0.5):
    """通用图像匹配并点击"""
    template = cv2.imread(template_path)
    match_result = match_template_with_color(img, template)
    
    if match_result:
        # 提取匹配点并缩放
        return True
    else:
        time.sleep(wait_time)
    return False

def texting(text,pos):
    """將文字打入手機"""
    coords = coordinates()
    found = False
    for x in text:
        if x in coords.alphabet:
            coords_value = coords.get_alphabet(x)
            found = True
        elif x in coords.capital:
            coords_value = coords.get_keyboard('shift')
            pos[0] = int(coords_value[0])
            pos[1] = int(coords_value[1])
            move(pos)
            time.sleep(0.3)
            click(pos)
            time.sleep(0.3)
            coords_value = coords.get_capital(x)
            found = True
        elif x in coords.number:
            coords_value = coords.get_number(x)
            found = True
        elif x in coords.keyboard:
            coords_value = coords.get_keyboard(x)
            found = True
        if found:
            pos[0] = int(coords_value[0])
            pos[1] = int(coords_value[1])
            move(pos)
            time.sleep(0.3)
            click(pos)
            found = False

        if x in coords.sign:
            transfer_value = coords.get_keyboard('transfer')
            pos[0] = int(transfer_value[0])
            pos[1] = int(transfer_value[1])
            move(pos)
            time.sleep(0.3)
            click(pos)
            time.sleep(0.3)
            coords_value = coords.get_sign(x)
            pos[0] = int(coords_value[0])
            pos[1] = int(coords_value[1])
            move(pos)
            time.sleep(0.3)
            click(pos)
            time.sleep(0.3)
            transfer_value = coords.get_keyboard('transfer')
            transfer_value = coords.get_keyboard('transfer')
            pos[0] = int(transfer_value[0])
            pos[1] = int(transfer_value[1])
            move(pos)
            time.sleep(0.3)
            click(pos)

        time.sleep(0.4)
    enter = coords.get_keyboard('enter')
    pos[0] = int(enter[0])
    pos[1] = int(enter[1])
    move(pos)
    time.sleep(0.3)
    click(pos)
    time.sleep(0.4)

def amounting(amount,pos):
    """將文字打入手機"""
    coords = coordinates()
    for x in amount:
        if x in coords.amount:
            coords_value = coords.get_amount(x)
        else:
            print('illegal amount')
            break
        pos[0] = int(coords_value[0])
        pos[1] = int(coords_value[1])
        move(pos)
        time.sleep(0.3)
        click(pos)
        time.sleep(0.3)
    enter = coords.get_keyboard('amount_enter')
    pos[0] = int(enter[0])
    pos[1] = int(enter[1])
    move(pos)
    time.sleep(0.3)
    click(pos)
    time.sleep(0.4)