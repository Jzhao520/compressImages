import os
import time
import click
import tinify
import threading
from tqdm import tqdm

# 每月免费500次 自己申请 自己申请 自己申请 重要的事情说三遍
online_key_list = [
    "abcdfghi"
]
# 获取压缩图片的KEY
online_key_list_iter = iter(online_key_list)
online_key = next(online_key_list_iter)

compressions_this_month = 0
__output_file_path__ = ''

# 通过调用tinify的API，实现一种无需上传即可压缩图片的方法
def compress_online(sourcefile, outputfile, name):
    global online_key
    global compressions_this_month
    global progess
    tinify.key = online_key
    tinify.validate()
    compressions_this_month = tinify.compression_count
    progess.set_description('压缩进行中图片' + name)
    time.sleep(0.2)
    print("当前剩余可用压缩次数：", 500 - compressions_this_month)
    fileName, fileSuffix = os.path.splitext(name)  # 分解文件名的扩展名
    rs = False
    try:
        source = tinify.from_file(sourcefile)
        source.to_file(outputfile + '/' + fileName + fileSuffix)
        rs = True
        pass
    except tinify.AccountError:
        # Verify your API key and account limit.
        online_key = next(online_key_list_iter)
        compress_online(sourcefile, outputfile, name)
        rs = True
        pass
    except tinify.ClientError:
        # Check your source image and request options.
        rs = False
        pass
    except tinify.ServerError:
        # Temporary issue with the Tinify API.
        rs = False
    except tinify.ConnectionError:
        # A network connection error occurred.
        print("网络故障。。。休息1秒继续")
        time.sleep(1)
        compress_online(sourcefile, outputfile, name)
        rs = True
        pass
    except Exception as e:
        print("Something else went wrong, unrelated to the Tinify API.")
        rs = False
        pass
    return rs


@click.command()
# 默认是根目录，支持传入自定义目录
@click.option('--source', default='./', help='待压缩的图片文件目录.')
@click.option('--output', default='./', help='已经压缩完成的图片文件目录.')
# 路径检测
def check_path_exists(source, output):
    global __output_file_path__
    # 检测输出路径是否是默认根路径 或者 是否是文件 example: E:\works\
    if output == './':
        # 检测文件夹是否存在，不存在就创建一个
        if not os.path.exists('./images') or os.path.exists('./images'):
            __output_file_path__ = './images'
    else:
        __output_file_path__ = output
    compress_hand(source, __output_file_path__)


# 支持压缩的图片格式 元组
fileSuffixTup = ('.png', '.jpg', '.jpeg', '.webp')


# 压缩文件时相关路径和支持图片格式识别处理
def compress_hand(source, output):
    global progess
    for root, dirs, files in os.walk(source):
        realpath = os.path.abspath(root)
        progess = tqdm(files)
        for name in progess:
            __path__ = os.path.join(realpath, name)

            fileName, fileSuffix = os.path.splitext(name)  # 分解文件名的扩展名
            if fileSuffix in fileSuffixTup:
                # 判断当前这个路径是否存在，如果不存在则创建一个
                if not os.path.exists(output):
                    os.mkdir(output)
                else:
                    pass
                if not compress_online(__path__, output, name):
                    print('压缩失败，检查报错信息')
                    exit()
                    pass
            else:
                pass


if __name__ == '__main__':
    t = threading.Thread(target=check_path_exists, args=())
    time.sleep(1)
    t.start()
