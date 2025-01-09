from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 加载预训练的GPT-2模型和对应的tokenizer
model_name = "gpt2-medium"  # 或者你可以选择其他GPT-2的模型，比如"gpt2"或"gpt2-large"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 输入文本，生成下一段文本
input_text = "今天天气不错，适合出去"
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# 生成文本
output = model.generate(input_ids, max_length=100, num_return_sequences=1, temperature=0.7)

# 解码生成的文本并打印输出
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("生成的文本：", generated_text)
