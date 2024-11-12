import torch

# 检查CUDA是否可用
if torch.cuda.is_available():
    # 获取GPU数量
    print(torch.cuda.device_count(), "个GPU可用：")
    # 打印每个GPU的名称
    for i in range(torch.cuda.device_count()):
        print(torch.cuda.get_device_name(i))
else:
    print("CUDA 不可用")
