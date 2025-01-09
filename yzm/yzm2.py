import cv2
import numpy as np
import pytesseract
from PIL import Image
import requests
from io import BytesIO


# 代码解释：
# 灰度化：将彩色图像转换为灰度图。
# 二值化：将灰度图转换为黑白图，以便更容易处理。
# 噪声去除：使用形态学变换去除小的噪声。
# 线条去除：通过检测水平和垂直线条并将其移除来减少干扰。
# 保存处理后的图像：保存预处理后的图像以便调试。
# 参数说明：
# cv2.threshold：用于二值化图像。
# cv2.morphologyEx：用于形态学变换，去除噪声和线条。
# cv2.erode 和 cv2.dilate：用于腐蚀和膨胀操作，分别用于线条检测和去除。
# --psm 6：Tesseract 的页面分割模式，选择适合你的图像的模式。

captcha_url = "http://127.0.0.1:9999/imgcode"  # 验证码图像的URL

# 设置 Tesseract 可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
def get_captcha_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise Exception("Failed to fetch captcha image")

# 读取图像
img = get_captcha_image(captcha_url)
img.save('path_to_image.jpg')
img = cv2.imread('path_to_image.jpg')

# 转换为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("../gray.png", gray)
# 二值化
# _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
# cv2.imwrite("binary.png",binary)
# # 噪声去除
# kernel = np.ones((1, 1), np.uint8)
# binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 自适应阈值
binary = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
)
cv2.imwrite("binary.jpg", binary)
text = pytesseract.image_to_string('binary.jpg')
print(text)
# 线条去除
# 1. 水平线条去除
horizontalsize = int(binary.shape[1] / 30)
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
horizontal = cv2.erode(binary, horizontalStructure, iterations=1)
horizontal = cv2.dilate(horizontal, horizontalStructure, iterations=1)
horizontal_inv = cv2.bitwise_not(horizontal)
binary = cv2.bitwise_and(binary, binary, mask=horizontal_inv)
cv2.imwrite("binary2.png", binary)
# 2. 垂直线条去除
verticalsize = int(binary.shape[0] / 30)
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
vertical = cv2.erode(binary, verticalStructure, iterations=1)
vertical = cv2.dilate(vertical, verticalStructure, iterations=1)
vertical_inv = cv2.bitwise_not(vertical)
binary = cv2.bitwise_and(binary, binary, mask=vertical_inv)
# 进一步去噪（可选）
# binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 保存处理后的图像以便调试
cv2.imwrite("binary3.png", binary)


# 将处理后的图像转换为 PIL 格式
preprocessed_img = Image.fromarray(binary)

# 使用 pytesseract 进行 OCR
text = pytesseract.image_to_string(preprocessed_img, config='--psm 6')
print(text)
