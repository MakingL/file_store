# file_store
---
## 简介
基于 `Python`  `Flask` 框架的文件存储管理，包括文件上传、下载、查询、删除
允许上传的文件格式：txt, pdf, png, jpg, jpeg, gif

## 环境
`Python 3.6.5`

## 安装
`pip install flask`

## 运行
`python flask_upload.py`

**默认端口号:** 8089

## 使用
1. 文件上传
`POST` 方法： `yourHost/upload` fileContent
2. 删除文件
`GET` 方法： `yourHost/delete` 参数：filename： yourFile (表单)
3. 下载文件
`GET` 方法： `yourHost/download/filename`
4. 获取服务器上的文件列表
`GET` 方法： `yourHost/getlist`
