# 上传到pipy

文件 ~/.pypirc
```
[distutils]
index-servers =
  pypi
  basin-pypi
 
#自己搭建的PyPI源信息
[basin-pypi]
repository:http://fz177:8082/nexus/repository/Python-yr/
username:pypi-uploader
password:pa44w0rd

[pypi]
repository:https://upload.pypi.org/legacy/
username:charlessoft
password:aA123456789ab

```
