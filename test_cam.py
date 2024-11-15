import requests
import cv2
import time
import threading
from coordinates import coordinates
import configparser
import json
from utils import unlock_screen, close_app, move, push, lift, click, stand_by, slide, match_and_wait, match_and_click, texting, amounting
import queue  # 引入队列模块，用于线程间通信
from appstate import appstate
from paddle_ocr import ocr_amount

def load_config():
    # 从 JSON 文件加载配置
    with open('hco.json', 'r') as json_file:
        hco = json.load(json_file)
    return hco 

def display_camera_feed(cap, event_queue, frame_queue):
    while True:
        # 擷取一幀畫面
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if not ret:
            print("無法擷取畫面")
            break

        # 将 frame 传递给主线程
        if frame_queue.full():  # 如果隊列已滿，刪除最舊的畫面
            frame_queue.get()  # 丟棄最舊的畫面
        frame_queue.put(frame)
        # 顯示畫面
        cv2.imshow('Camera Feed', frame)

        # 按下 'q' 鍵退出
        key = cv2.waitKey(1)  # 每次按键时暂停1ms等待
        if key & 0xFF == ord('q'):
            event_queue.put('q')
            break

        # 传递其他按键事件到主线程
        elif key & 0xFF == ord('d'):
            event_queue.put('d')
        elif key & 0xFF == ord('s'):
            event_queue.put('s')
        elif key & 0xFF == ord('a'):
            event_queue.put('a')
        elif key & 0xFF == ord('w'):
            event_queue.put('w')
        elif key & 0xFF == ord('f'):
            event_queue.put('f')
        elif key & 0xFF == ord('r'):
            event_queue.put('r')
        elif key & 0xFF == ord('z'):
            event_queue.put('z')
        elif key & 0xFF == ord('l'):
            event_queue.put('l')
        elif key & 0xFF == ord('o'):
            event_queue.put('o')

    # 釋放相機並關閉所有視窗
    cap.release()
    cv2.destroyAllWindows()

# 主程式部分
coords = coordinates()
config = configparser.ConfigParser()
config.read('account_ACB.ini')
locknumber = config['Account']['locknumber']
username = config['Account']['username']
password = config['Account']['password']
bank = config['Account']['bank']
baccount = config['Account']['baccount']
amount = config['Account']['amount']
pingcode = config['Account']['pingcode']
state = appstate()
templates_folde = "./ACB_templates/"
pos = [0, 0, 0]
move(pos)
hand_mode = False

# 開啟相機
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法打開相機")
    exit()

# 用於傳遞事件的隊列
event_queue = queue.Queue()
frame_queue = queue.Queue(maxsize=5)  # 用於传递 frame 数据的队列

# 在另一個线程中顯示相機畫面
display_thread = threading.Thread(target=display_camera_feed, args=(cap, event_queue, frame_queue))
display_thread.start()

while True:
    try:
        # 监听按键事件
        key_event = event_queue.get(timeout=0.1)  # 设置超时防止阻塞
    except queue.Empty:
        key_event = None

    # 读取最新的 frame
    if not frame_queue.empty():
        if not hand_mode:
            pos = stand_by()
        frame = frame_queue.get()
    else:
        frame = []
        continue


    if state.machine_on:

        if match_and_wait(frame,templates_folde+'loading1'+'.png',0):
            print('loading')
            continue
        if match_and_wait(frame,templates_folde+'loading2'+'.png',0):
            print('loading')
            continue
        if match_and_wait(frame,templates_folde+'loading3'+'.png',0):
            print('loading')
            continue

        if state.pingcode_start and not state.ping_done:
            if match_and_wait(frame,templates_folde+'16'+'.png'):
                amounting(pingcode, pos)
                print('ping code done')

        if state.confirm_done and not state.pingcode_start:
            if match_and_wait(frame,templates_folde+'15'+'.png'):
                if match_and_click(frame,templates_folde+'15'+'.png', pos):
                    state.pingcode_start = True
                    print('start ping code')
            else:
                state.confirm_end = False


        if state.continue_done and not state.confirm_done:
            if match_and_wait(frame,templates_folde+'14'+'.png'):
                state.confirm_done = True
                ocr_amount(frame, 'en')
                print("confirm")
                pos = [30, -30, 0]
                pos = slide(pos,[pos[0],pos[1]-120,pos[2]])
            

        if state.amount_done and not state.continue_done:
            if match_and_wait(frame,templates_folde+'13'+'.png'):
                if match_and_click(frame,templates_folde+'13'+'.png',pos):
                    state.continue_done = True
                    print('continue!')
                 
        if state.kbping_done and not state.amount_done:
            if match_and_wait(frame,templates_folde+'12_2'+'.png'):
                amounting(amount, pos)
                time.sleep(0.5)
                pos = [30, -30, 0]
                pos = slide(pos,[pos[0],pos[1]-60,pos[2]])
                state.amount_done = True
                print("amount done")
            else:
                if match_and_wait(frame,templates_folde+'12_1'+'.png'):
                    state.kbping_done = False

        if  state.baccount_done and not state.kbping_done:
            if match_and_wait(frame,templates_folde+'12_1'+'.png'):
                if match_and_click(frame,templates_folde+'12_1'+'.png', pos):
                    print("typing amount")
                    state.kbping_done = True


        if  state.kbbaccount_done and not state.baccount_done:
            if match_and_wait(frame,templates_folde+'11_2'+'.png'):
                texting(baccount, pos)
                print("baccount keyboard")
                state.baccount_done = True
            else:
                if match_and_wait(frame,templates_folde+'11_1'+'.png'):
                    state.kbbaccount_done = False
        
        if  state.bank_type and not state.kbbaccount_done:
            if match_and_wait(frame,templates_folde+'11_1'+'.png'):
                if match_and_click(frame,templates_folde+'11_1'+'.png', pos):
                    print("typing baccount")
                    state.kbbaccount_done = True

        if  state.bank_search and not state.bank_type:
            if match_and_wait(frame,templates_folde+'10'+'.png'):
                    texting(bank,pos)
                    print("end typing")
                    pos[0]=32
                    pos[1]=-95
                    pos[2]=0
                    move(pos)
                    click(pos)
                    state.bank_type = True
            else:
                state.bank_done = False

        if state.bank_select and not state.bank_search:
            if match_and_wait(frame,templates_folde+'9'+'.png'):
                if match_and_click(frame,templates_folde+'9'+'.png', pos):
                    state.bank_search = True
                    print("start bank search")
            else:
                state.bank_select = False

        if state.app_transfer and not state.bank_select:
            if match_and_wait(frame,templates_folde+'8'+'.png'):
                if match_and_click(frame,templates_folde+'8'+'.png', pos):
                    state.bank_select = True
                print("start bank select")
            else:
                if match_and_wait(frame,templates_folde+'7'+'.png'):
                    state.app_transfer = False

        if state.app_dash and not state.app_transfer:
            if not match_and_wait(frame,templates_folde+'7'+'.png'):
                print("dashboard loading!")
                time.sleep(1)
                state.app_dash = False
            else:
                if  match_and_click(frame,templates_folde+'7'+'.png',pos):
                    print('transfer go!')
                    state.app_transfer = True

    #.........
        if state.app_logged and not state.app_dash:
            if not match_and_wait(frame,templates_folde+'6_1'+'.png'):
                print("typing not yet!")
            else:
                if match_and_click(frame,templates_folde+'6_2'+'.png',pos):
                    print('dash board')
                    state.app_dash = True

        if state.password_kb and not state.app_logged:
            if not match_and_wait(frame,templates_folde+'5'+'.png'):
                print("typing not yet!")
            else:
                if match_and_click(frame,templates_folde+'5'+'.png',pos):
                    print('typing done!')
                    state.app_logged = True

        if state.app_password and not state.password_kb:
            if not match_and_wait(frame,templates_folde+'4'+'.png'):
                print("password keyboard not yet!")
            else:
                texting(password, pos)
                print('typing!')
                state.password_kb = True

        if state.login and not state.app_password:
            if not match_and_wait(frame,templates_folde+'3'+'.png'):
                print("password not yet!")
            else:
                if match_and_click(frame,templates_folde+'3'+'.png',pos):
                    print('start password')
                    state.app_password = True

        if state.app_on and not state.login:
            if not match_and_wait(frame,templates_folde+'2_1'+'.png'):
                print("login not yet!")
                if match_and_click(frame,templates_folde+'ACB'+'.png',pos):
                    print('click app again')
            else:
                if match_and_click(frame,templates_folde+'2_2'+'.png',pos):
                    print('start password')
                    state.login = True


        if state.machine_on and not state.app_on:
            print(state.app_on)
            if not match_and_wait(frame,templates_folde+'ACB'+'.png'):
                    pos = stand_by()
                    pos[0]= 60
                    move(pos)
                    time.sleep(0.5)
                    pos2 = pos.copy()
                    pos2[0] = 0
                    pos = slide(pos, pos2)
                    time.sleep(1)
                    pos = stand_by()

            else:
                print('found!')
                if match_and_click(frame,templates_folde+'ACB'+'.png',pos):
                    print('click!')
                    state.app_on = True
            

    if key_event:
        if key_event == 'q':
            pos = [0, 0, 0]
            move(pos)
            print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')
            break

        elif key_event == 'd':
            if pos[0] < 65:
                pos[0] = pos[0] + 1
                move(pos)
                print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 's':
            if pos[1] < 0:
                pos[1] = pos[1] + 1
                move(pos)
                print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'a':
            #if pos[0] > 0:
            if True:
                pos[0] = pos[0] - 1
                move(pos)
                print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'w':
            if pos[1] > -165:
                pos[1] = pos[1] - 1
                move(pos)
                print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'r':
            click(pos)
            print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'z':
            hand_mode = not hand_mode
            pos = [0, 0, 0]
            move(pos)
            print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'f':
            pos = [0, -70, 0]
            move(pos)
            time.sleep(1)
            pos2 = pos
            pos2[0] = pos[0] + 60
            pos = slide(pos, pos2)
            time.sleep(2)
            pos2[0] = pos[0] - 60
            pos = slide(pos2, pos)
            print(f'x:{pos[0]} y:{pos[1]} z{pos[2]}')

        elif key_event == 'l':
            pos = unlock_screen()
            close_app()
        elif key_event == 'o':
            state.machine_on = not state.machine_on

# 等待顯示线程结束
display_thread.join()
