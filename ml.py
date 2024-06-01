import json
import re
import time

# 读取JSON数据集
input_path = 'test.json'
with open(input_path, 'r') as file:
    data = json.load(file)

# 解析问题和答案的函数
def parse_questions_answers(entry):
    # 使用正则表达式查找问题-答案对
    qa_pairs = re.findall(r'Headline: .*?\? (Yes|No)', entry)
    questions = re.findall(r'Headline: .*? (Now answer this question:|Question:|Does the news headline talk about|Please answer a question about the following headline:) (.*?)( Yes| No|$)', entry)
    return [{"question": q[1].strip(), "answer": a} for q, a in zip(questions, qa_pairs)]

# 创建一个列表来存储重新格式化的数据
reformatted_data = []
unique_id = 1

# 处理数据集中的每个条目
start_time = time.time()
for entry in data:
    qa_pairs = parse_questions_answers(entry["input"])
    for qa in qa_pairs:
        reformatted_data.append({
            "id": unique_id,
            "Question": qa["question"],
            "Answer": qa["answer"],
            "class_id": entry["class_id"]
        })
        unique_id += 1
end_time = time.time()

# 将重新格式化的数据保存到JSON文件
output_path = 'reformatted_dataset.json'
with open(output_path, 'w') as json_file:
    json.dump(reformatted_data, json_file, indent=4)

# 报告统计数据和性能指标
total_qa_pairs = len(reformatted_data)
processing_time = end_time - start_time

print(f"Total Question-Answer Pairs: {total_qa_pairs}")
print(f"Processing Time: {processing_time:.2f} seconds")
