import cv2
import numpy as np
import pytesseract
from PIL import Image

# 设置 Tesseract 可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# 读取图像
img_path = 'binary.png'
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# 二值化
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 去除小的噪声
kernel = np.ones((3, 3), np.uint8)
cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

# 检测轮廓
contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
# 创建一个空白图像用于绘制检测到的轮廓
detected_numbers = np.zeros_like(img)

# 过滤并绘制轮廓
for contour in contours:
    if cv2.contourArea(contour) > 100:  # 根据面积过滤噪声
        x, y, w, h = cv2.boundingRect(contour)
        detected_numbers = cv2.drawContours(detected_numbers, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
# 将处理后的图像转换为 PIL 格式
preprocessed_img = Image.fromarray(detected_numbers)
print(detected_numbers)
cv2.imwrite('sdfdf.png', preprocessed_img)
# 使用 pytesseract 进行 OCR
text = pytesseract.image_to_string(preprocessed_img, config='--psm 6')
print("识别结果:", text)
