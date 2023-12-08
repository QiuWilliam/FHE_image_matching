# 数据安全第二次作业
我选择了tenseal这个开源库，通过实现图像匹配来验证CKKS和BFV在加密解密时间上的差异。TenSEAL是一个具有Python接口的C++库。这个库有两个好处。一个是安装比SEAL省心，直接 pip install tenseal 就可以运行了。另一个是不需要过多地考虑CKKS、BFV的实现细节（比如矩阵乘法的底层细节），直接调用接口就可以实现运算了。

query.jpg是需要匹配的图片，dataset是文件系统，里面共有5张图片，用于和query.jpg进行匹配
所采用的数据集为ImageNet的64×64的图片

只需运行两个py文件，就可以得到加密解密时间，以及匹配的指标MSE
