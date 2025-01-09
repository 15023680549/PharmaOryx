import requests
from PIL import Image
import pytesseract
from io import BytesIO


# 说明：
# 1.获取验证码图像：使用requests库从指定的URL获取验证码图像。
# 2.图像预处理：对图像进行灰度化和二值化处理，以提高OCR的识别率。
# 3.验证码识别：使用pytesseract库将图像中的文本识别出来。
# 4.提交识别结果：将识别出的验证码和其他表单数据提交到目标网站。

# 配置Tesseract路径（如果需要）
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def get_captcha_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise Exception("Failed to fetch captcha image")

def preprocess_image(img):
    # 可以在这里添加图像预处理代码，例如灰度化，二值化等
    # 下面是一个简单的示例
    img = img.convert('L')  # 转为灰度图
    img = img.point(lambda x: 0 if x < 128 else 255)  # 二值化
    return img

def solve_captcha(img):
    text = pytesseract.image_to_string(img)
    return text.strip()

def submit_captcha_solution(solution, submit_url, data):
    data['captcha'] = solution
    response = requests.post(submit_url, data=data)
    return response

# 示例用法
captcha_url = "http://127.0.0.1:9999/imgcode"  # 验证码图像的URL
submit_url = "https://example.com/submit"  # 提交验证码的URL
data = {"username": "your_username", "password": "your_password"}

# 获取验证码图像
img = get_captcha_image(captcha_url)
print(img)

# 打开图像并转换为 JPG 格式
img = img.convert('RGB')
img.save('path_to_image.jpg')
# 使用 pytesseract 进行 OCR
text = pytesseract.image_to_string('path_to_image.jpg')
print(text)

# 预处理图像
preprocessed_img = preprocess_image(img)
print(preprocessed_img)
# 识别验证码
captcha_solution = solve_captcha(preprocessed_img)
print(captcha_solution)
# # 提交验证码和其他数据
response = submit_captcha_solution(captcha_solution, submit_url, data)

# 检查响应
if response.status_code == 200:
    print("Captcha solved and form submitted successfully!")
else:
    print("Failed to submit form.")
