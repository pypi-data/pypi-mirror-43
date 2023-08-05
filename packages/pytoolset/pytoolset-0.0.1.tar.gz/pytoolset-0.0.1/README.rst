
在本地目录执行以下命令应该能成功在dist目录下生成 tar.gz 结尾的文件
python setup.py sdist 
如果需要whl文件，则执行下面这个
python setup.py sdist bdist_wheel


需要到pypi注册并验证包以后才能真正上传，使用下面的方法注册:
twine upload dist/*
注意register命令已经不被支持了 


发布轮子:
python setup.py register sdist upload: 这个不安全，应该使用下面这个：
twine upload dist/*


