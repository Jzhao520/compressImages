## 命令行图片压缩工具
[tinypng API key 申请](https://tinypng.com/developers)

[![python3.7](https://img.shields.io/badge/pyhotn3.7-jianzhao151-green)](https://shields.io/)

### 使用方法
- 指定源，输入文件默认根目录, 压缩完成后文件在 <span style="font-weight: bold;text-align:left;color:#00ff00;">./images文件中</span>
> python main.py --source="E:\works\file"

- 同时指定源和输出目录, 压缩完成后文件在 <span style="font-weight: bold;text-align:left;color:#00ff00;">output指定的目录中</span>
> python main.py --source="E:\works\file" --output="E:\works\aaa"

### 测试用例

> python main.py --source="E:\works\file"

> python main.py --source="E:\works\file" --output="E:\works\"
 
> python main.py --source="E:\works\file" --output="E:\works\a"

