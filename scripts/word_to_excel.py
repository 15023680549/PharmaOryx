from docx import Document
import pandas as pd
import re


# 提取文本数据
def parse_policy_text(filename):
    document = Document(filename)
    data = []
    policy_type = ""  # 记录政策类型
    policy_name = ""  # 记录政策名称
    record = {}  # 存储单条政策数据
    current_key = None  # 当前记录的字段

    # 定义需要提取的字段
    fields = ["政策依据", "支持行业", "政策内容及标准", "咨询单位及科室", "联系人", "政策执行期限", "申报流程", "申报材料", "办理地点"]

    for para in document.paragraphs:
        text = para.text.strip()  # 读取段落内容并去掉前后空格

        if not text:
            continue  # 跳过空行

        # 识别政策类型（如：一、二、三、四...二十一等）
        if re.match(r"^[一二三四五六七八九十百]+[一二三四五六七八九十]?、", text):
            if record:
                data.append(record)  # 保存之前的记录
                record = {}  # 清空记录
            policy_type = text.split("、", 1)[1].strip()  # 提取政策类型标题
            current_key = None  # 重置当前字段
            continue

        # 识别政策名称
        if text.startswith("（") and "）" in text:
            if record:
                data.append(record)  # 保存之前的记录
                record = {}  # 清空记录
            policy_name = text.strip()
            record = {"政策类型": policy_type, "政策名称": policy_name}
            current_key = None  # 重置当前字段
            continue
        # 提取具体内容
        elif "政策依据" in text:
            current_key = "政策依据"
            record["政策依据"] = text.split("：", 1)[1].strip()
            continue
        elif "支持行业" in text:
            current_key = "支持行业"
            record["支持行业"] = text.split("：", 1)[1].strip()
            continue
        elif "政策内容及标准" in text:
            current_key = "政策内容及标准"
            record["政策内容及标准"] = text.split("：", 1)[1].strip()
            continue
        elif "咨询单位及科室" in text or "咨询部门":
            current_key = "咨询单位及科室"
            print(record)
            print(text)
            record[current_key] = text.split("：", 1)[1].strip()
            continue
        # elif text.startswith("5.") and "联系人" in text:
        elif "联系人" in text:
            current_key = "联系人"
            record["联系人"] = text.split("：", 1)[1].strip()
            continue
        elif "政策执行期限" in text:
            current_key = "政策执行期限"
            record["政策执行期限"] = text.split("：", 1)[1].strip()
            continue
        elif "申报流程" in text:
            current_key = "申报流程"
            print(record)
            record["申报流程"] = text.split("：", 1)[1].strip()
            continue
        elif "申报材料" in text:
            current_key = "申报材料"
            record["申报材料"] = text.split("：", 1)[1].strip()
            continue
        elif "办理地点" in text:
            current_key = "办理地点"
            record["办理地点"] = text.split("：", 1)[1].strip()
            continue

        # 追加多段内容到当前字段
        if current_key:
            record[current_key] += f"\n{text}"

        # 定义需要提取的字段
        field_patterns = {
            "政策依据": r"政策依据[:：](.*?)(?=(支持行业|政策内容及标准|咨询单位及科室|联系人|$))",
            "支持行业": r"支持行业[:：](.*?)(?=(政策内容及标准|咨询单位及科室|联系人|$))",
            "政策内容及标准": r"政策内容及标准[:：](.*?)(?=(咨询单位及科室|联系人|$))",
            "咨询单位及科室": r"咨询单位及科室[:：](.*?)(?=(联系人|$))",
            "联系人": r"联系人[:：](.*)"
        }

        # 匹配字段内容
        for key, pattern in field_patterns.items():
            match = re.search(pattern, text, re.S)
            if match:
                record[key] = match.group(1).strip()

    # 最后一条记录追加
    if record:
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
