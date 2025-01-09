from docx import Document
import pandas as pd
import re


# def extract_text_from_pdf(filename):
#     """提取PDF中的文本"""
#     pdf_document = fitz.open(filename)
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document[page_num]
#         text += page.get_text("text")  # 按文本顺序提取
#     pdf_document.close()
#     return text

# 提取文本数据
def parse_policy_text(filename):
    document = Document(filename)
    data = []
    policy_type = ""  # 当前政策类型
    policy_name = ""  # 当前政策名称
    record = {}  # 单条政策记录

    # 定义需要提取的字段和别名映射
    fields = ["政策依据", "支持行业", "政策内容及标准", "咨询单位及科室", "联系人", "政策执行期限", "申报流程", "申报材料", "办理地点", "联系电话"]
    alias_mapping = {
        "政策内容及标准":["政策内容及标准", "政策内容标准"],
        "联系电话": ["联系电话", "咨询电话","电话"],
        "支持行业":["支持行业", "补贴对象"]
    }

    # 合并所有段落，便于按政策块处理
    all_text = "\n".join([para.text.strip() for para in document.paragraphs if para.text.strip()])
    #从word获取改为pdf获取
    # all_text = extract_text_from_pdf(filename)

    # 使用政策类型正则表达式拆分
    type_blocks = re.split(r"^[一二三四五六七八九十百]+[一二三四五六七八九十]?、", all_text, flags=re.M)
    type_blocks = [block.strip() for block in type_blocks if block.strip()]  # 去除空白块

    # 逐块处理
    for type_block in type_blocks:
        # 按政策类型分块
        policy_type = type_block.split("\n", 1)[0].strip()

        # 按政策名称分块
        name_blocks = re.split(r"（[一二三四五六七八九十]+）", type_block)
        name_blocks = [block.strip() for block in name_blocks if block.strip()]

        for i, name_block in enumerate(name_blocks):
            if i==0:
                continue
            #提取政策名称,第一行
            policy_name = name_block.split("\n", 1)[0].strip()
            record = {"政策类型": policy_type, "政策名称": policy_name}

            # 提取字段内容
            for field in fields:
                # 获取字段的别名（包括自身）
                all_aliases = [field] + alias_mapping.get(field, [])
                alias_pattern = "|".join([f"{alias}[:：]" for alias in all_aliases])

                # 动态生成正则表达式
                next_fields = [f"{f}[:：]" for f in fields if f != field]
                next_field_pattern = "|".join(next_fields) if next_fields else "$"
                pattern = rf"({alias_pattern})(.*?)(?={next_field_pattern}|\Z)"

                # 在当前块中搜索匹配
                match = re.search(pattern, name_block, re.S)
                if match:
                    record[field] = match.group(2).strip()

            data.append(record)

    return data

# 保存到Excel
def save_to_excel(data, output_filename):
    df = pd.DataFrame(data)
    df.to_excel(output_filename, index=False)

# 主程序
if __name__ == "__main__":
    input_file = "重庆市江津区2024年惠企政策汇编.docx"  # 替换为你的Word文件路径
    output_file = "重庆市江津区2024年惠企政策汇编.xlsx"  # 生成的Excel文件名

    data = parse_policy_text(input_file)
    save_to_excel(data, output_file)
    print(f"数据已成功保存到 {output_file}")
