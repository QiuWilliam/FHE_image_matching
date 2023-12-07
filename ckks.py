import time
import os
from PIL import Image
import numpy as np

import tenseal as ts


def create_ctx():
    context = ts.context(ts.SCHEME_TYPE.CKKS, 16384, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = pow(2, 40)
    context.generate_galois_keys()
    return context


# Sample an image
def load_input(img_name):
    img = Image.open(img_name)
    # 转换为NumPy数组
    img_array = np.array(img)

    img_vector = img_array.flatten()

    return img_vector

def load_images_from_folder(folder_path):
    img_vectors = []  # 用于存储图像向量的列表

    for filename in os.listdir(folder_path):
        # 检查文件是否是图像文件（你可能需要根据实际情况添加更多的文件格式）
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(folder_path, filename)
            img_vector = load_input(img_path)
            img_vectors.append(img_vector)

    return img_vectors


def MMSE(ori, tar):
    temp = ori - tar
    result = temp * temp
    result1 = result.sum()
    return result1


context = create_ctx()
query = load_input('query.jpg')
data = load_images_from_folder('dataset')

##加密部分
times = time.time()

encrypted_query = ts.ckks_vector(context, query)

print("query图像的加密时间为{}".format(time.time() - times))  # 加密时间=3.856888771057129

encrypteds = []
for i, img_vector in enumerate(data):

    times = time.time()

    encrypteds.append(ts.ckks_vector(context, img_vector))

    print("文件系统中第{}张图像的加密时间为{}".format(i+1, time.time() - times))

##开始计算MSE
results = []

for i, encrypted in enumerate(encrypteds):

    temp = MMSE(encrypted_query, encrypted)
    t = time.time()
    result = temp.decrypt()  #解密结果
    timeend = time.time() - t

    result = np.array(result) / 3 / 4096 #明文进行除法
    results.append(result)
    print("文件系统中第{}张图片匹配得到的MSE为{},其解密时间为{}".format(i+1,result,timeend))


# 找到最小值
min_value = np.min(results)

# 找到最小值的下标
min_index = np.argmin(results)

print("得到的最小MSE为{},是第{}张图片".format(min_value, min_index+1))