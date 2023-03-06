# holochat

1. 保证安装了python环境(python>=3.8)和Django包
2. 部署机器能够科学访问外网
3. 下载holochat代码库
4. 设置环境变量，以Linux环境为例:
```
   export OPENAI_ORG=YOUR_ORG
   export OPENAI_KEY=YOUR_KEY
```
5. 在holochat目录下创建`database`目录, 创建`chat.sqlite3`文件作为数据库存储聊天记录, 格式化数据
```
    python manage.py sqlmigrate chatgpt_proxy 0001 
```
6. 启动Django
```
   python manage.py runserver
```
