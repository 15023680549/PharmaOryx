from transformers import pipeline

# 创建基于Hugging Face的transformers预训练模型
qa_pipeline = pipeline("question-answering")

# 基于检索的问题-答案对
qa_pairs = {
    "什么是人工智能?": "人工智能是模拟人类智能的一种技术。",
    "有哪些人工智能的应用?": "人工智能应用包括语音识别、图像识别、自然语言处理等。",
    "机器学习是什么?": "机器学习是一种人工智能的技术，让机器能够从数据中学习和改进。",
    # 可以根据需要添加更多的问题和答案
}

def retrieve_based_qa(question):
    for key, value in qa_pairs.items():
        if question.lower() in key.lower():
            return value
    return None

def answer_question(question):
    # 首先尝试从基于检索的问答对中获取答案
    retrieved_answer = retrieve_based_qa(question)
    if retrieved_answer:
        return retrieved_answer

    # 如果未从基于检索的问答对中找到答案，则尝试使用预训练模型进行问答
    try:
        answer = qa_pipeline(question=question, context="")
        return answer['answer']
    except Exception as e:
        print(f"出现错误：{e}")
        return "抱歉，我暂时无法回答您的问题。"

# 测试问答系统
while True:
    user_question = input("请输入您的问题 (输入 '退出' 来结束): ")
    if user_question == '退出':
        break
    answer = answer_question(user_question)
    print("答案:", answer)
