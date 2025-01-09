import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import ne_chunk, pos_tag

# 下载NLTK的Punkt tokenizer和averaged_perceptron_tagger资源
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# 用于存储问题-答案对的字典
qa_pairs = {
    "什么是人工智能?": "人工智能是模拟人类智能的一种技术。",
    "有哪些人工智能的应用?": "人工智能应用包括语音识别、图像识别、自然语言处理等。",
    "机器学习是什么?": "机器学习是一种人工智能的技术，让机器能够从数据中学习和改进。",
    # 可以根据需要添加更多的问题和答案
}

def preprocess_sentence(sentence):
    # 分词并去除停用词
    tokens = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens

def get_answer(question):
    tokens = preprocess_sentence(question)
    for key, value in qa_pairs.items():
        if all(token.lower() in preprocess_sentence(key) for token in tokens):
            return value
    return "抱歉，我暂时无法回答您的问题。"

# 测试问答系统
while True:
    user_question = input("请输入您的问题 (输入 '退出' 来结束): ")
    if user_question == '退出':
        break
    answer = get_answer(user_question)
    print("答案:", answer)
