import cv2
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import re

def preprocess_image(image):
    # 讀取圖像
    
    # 1. 轉為灰階圖像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. 去噪：使用高斯模糊
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. 使用 Otsu 方法進行二值化
    #_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 4. 可選：直方圖均衡化（增強對比度）
    #equalized = cv2.equalizeHist(gray)
    
    return gray

def ocr_and_draw_text(image, font_path="c:/Windows/Fonts/simsun.ttc", text_size=20, text_color=(255, 0, 0)):
    image = preprocess_image(image)
    # 初始化 PaddleOCR
    ocr = PaddleOCR(lang='en')
    # 讀取圖片
    otp_number = '000000'
    # 執行 OCR
    result = ocr.ocr(image, cls=True)
    pattern = r'OTP.*(\d{6})'  # 匹配 OTP 之後的六位數字
    # 遍歷每個識別結果
    for line in result[0]:
        # 獲取文字的邊界框座標和內容
        text = line[1][0]
        # 正則表達式：匹配 OTP 後的六位數
        # 使用 re.search 找到匹配的數字
        match = re.search(pattern, text)

        if match:
            otp_number = match.group(1)  # 提取匹配到的六位數字
            print("OTP number found:", otp_number)
        else:
            print("OTP number not found")
    return otp_number

def ocr_otp(image, language):
    # 初始化 PaddleOCR
    image = preprocess_image(image)
    ocr = PaddleOCR(lang=language)

    # 讀取圖片
    otp_number = 'XXXXXX'
    # 執行 OCR
    result = ocr.ocr(image, cls=True)
    pattern = r'OTP.*(\d{6})'  # 匹配 OTP 之後的六位數字
    # 遍歷每個識別結果
    for line in result[0]:
        # 獲取文字的邊界框座標和內容
        text = line[1][0]
        # 正則表達式：匹配 OTP 後的六位數
        # 使用 re.search 找到匹配的數字
        match = re.search(pattern, text)

        if match:
            otp_number = match.group(1)  # 提取匹配到的六位數字
            print("OTP number found:", otp_number)
    return otp_number

import re
from paddleocr import PaddleOCR

def ocr_amount(image, language):
    # 初始化 PaddleOCR
    image = preprocess_image(image)
    ocr = PaddleOCR(lang=language)

    # 讀取圖片
    amount_number = ''
    # 執行 OCR
    result = ocr.ocr(image, cls=True)

    # 打印 OCR 識別結果，查看結果的格式
    print("OCR result:", result)

    # 用於匹配包含逗號的數字，在 VND 前
    pattern = r'([\d,]+)(?=\s*VND)'

    # 遍歷每個識別結果
    for line in result[0]:
        # 獲取文字的邊界框座標和內容
        text = line[1][0]

        # 使用正則表達式匹配 VND前的數字
        match = re.search(pattern, text)

        if match:
            amount_number = match.group(1)  # 提取匹配到的金額（可能包含逗號）
            print("Amount number found:", amount_number)

    return amount_number





