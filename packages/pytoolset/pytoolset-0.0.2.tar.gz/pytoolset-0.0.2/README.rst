
在本地目录执行以下命令应该能成功在dist目录下生成 tar.gz 结尾的文件
python setup.py sdist 
如果需要whl文件，则执行下面这个
python setup.py sdist bdist_wheel


现在已经不需要注册了，所以用以下命令直接发布就可以:
twine upload dist/*
注意register命令已经不被支持了 


