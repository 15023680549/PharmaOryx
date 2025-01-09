import pyocr
import pyocr.builders
from PIL import Image

# 初始化OCR引擎
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    exit(1)
ocr_tool = tools[0]

# 打开图像文件
image = Image.open('path_to_image.jpg')

# 使用OCR引擎进行文本识别
text = ocr_tool.image_to_string(
    image,
    lang='eng',
    builder=pyocr.builders.TextBuilder()
)

# 打印识别结果
print(text)