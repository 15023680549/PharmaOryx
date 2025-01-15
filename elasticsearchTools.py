from elasticsearch import Elasticsearch

es = Elasticsearch('http://127.0.0.1:9200/')
print(es.ping)

# 创建索引
# es.indices.create(index="my_index2")

# 删除索引
# es.indices.delete(index="my_index")

# 检查索引是否存在
es.indices.exists(index="my_index")

# 添加文档
doc1 = {
    "title": "测试文档1",
    "content": "这是一个测试文档1",
    "timestamp": "2024-12-07"
}
doc2 = {
    "title": "测试文档2",
    "content": "这是一个测试文档2",
    "timestamp": "2024-12-01"
}
# 指定ID插入
es.index(index="my_index2", id="1", body=doc1)
# 自动生成ID插入
es.index(index="my_index2", body=doc2)

# 获取文档
result = es.get(index="my_index2", id="1")
print(result)

# 更新文档
update_doc = {
    "doc": {
        "title": "更新后的标题"
    }
}
es.update(index="my_index2", id="1", body=update_doc)
print(es.get(index="my_index2", id="1"))

# 删除文档
es.delete(index="my_index2", id="1")