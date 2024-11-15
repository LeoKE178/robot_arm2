import cv2
import numpy as np

def calculate_histogram(image):
    # 將圖像轉換為 HSV 顏色空間
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 計算顏色直方圖
    hist = cv2.calcHist([hsv_image], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist

def bhattacharyya_distance(hist1, hist2):
    # 計算 Bhattacharyya 距離
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

def match_template_with_color(image, template):
    # 計算模板的顏色直方圖
    template_hist = calculate_histogram(template)
    
    # 對圖像進行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.6  # 相似度閾值

    # 尋找匹配位置
    locations = np.where(result >= threshold)

    
    matches = []
    for pt in zip(*locations[::-1]):  # 反轉以獲取 x, y 坐標
        # 提取當前匹配區域的顏色直方圖
        roi = image[pt[1]:pt[1]+template.shape[0], pt[0]:pt[0]+template.shape[1]]
        roi_hist = calculate_histogram(roi)
        
        # 計算顏色相似度
        distance = bhattacharyya_distance(template_hist, roi_hist)
        # 如果顏色相似度低於閾值，則視為有效匹配
        if distance < 1:  # 自定義顏色相似度閾值
            matches.append(pt)

    return matches

def match_template_with_color_low_threshold(image, template):
    # 計算模板的顏色直方圖
    template_hist = calculate_histogram(template)
    
    # 對圖像進行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.45  # 相似度閾值

    # 尋找匹配位置
    locations = np.where(result >= threshold)

    
    matches = []
    for pt in zip(*locations[::-1]):  # 反轉以獲取 x, y 坐標
        # 提取當前匹配區域的顏色直方圖
        roi = image[pt[1]:pt[1]+template.shape[0], pt[0]:pt[0]+template.shape[1]]
        roi_hist = calculate_histogram(roi)
        
        # 計算顏色相似度
        distance = bhattacharyya_distance(template_hist, roi_hist)
        # 如果顏色相似度低於閾值，則視為有效匹配
        if distance < 1.5:  # 自定義顏色相似度閾值
            matches.append(pt)

    return matches
