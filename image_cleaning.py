import cv2
import numpy as np

# 計算清洗成功機率的輔助函數
def calculate_cleaning_success_probability(image_path):
    # 讀取圖片
    image = cv2.imread(image_path)
    
    # 檢查圖片是否加載成功
    if image is None:
        print("Error: Image not found.")
        return None
    
    # 將圖片轉為灰度圖
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 計算圖片的平均亮度
    avg_brightness = np.mean(gray)
    
    # 假設亮度越高，清洗成功機率越高，這裡使用亮度來模擬成功機率
    success_probability = min(100, avg_brightness)  # 假設最大為 100
    
    return success_probability

# 用正確的圖片路徑來測試
result = calculate_cleaning_success_probability("C:/Users/lin/Desktop/stain-analysis/uploads/20231101224307-7c77dd59.jpg")
if result is not None:
    print(f"Cleaning success probability: {result}%")
