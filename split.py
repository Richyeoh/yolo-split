import os
import shutil
import random


def copy_files(file_pairs, src_img_dir, src_lbl_dir, dst_img_dir, dst_lbl_dir):
    """复制文件到指定目录"""
    for img_file, lbl_file in file_pairs:
        # 复制图像文件
        shutil.copy(
            os.path.join(src_img_dir, img_file),
            os.path.join(dst_img_dir, img_file)
        )
        # 复制标签文件
        shutil.copy(
            os.path.join(src_lbl_dir, lbl_file),
            os.path.join(dst_lbl_dir, lbl_file)
        )


if __name__ == '__main__':
    # 配置参数
    split_ratio = [0.7, 0.2, 0.1]  # train/val/test

    # 数据集路径
    dataset_root = './datasets/ads'
    image_dir = os.path.join(dataset_root, 'images')
    label_dir = os.path.join(dataset_root, 'labels')

    # 获取并验证文件列表
    image_files = sorted(os.listdir(image_dir))
    label_files = sorted(os.listdir(label_dir))

    # 验证文件数量匹配
    if len(image_files) != len(label_files):
        raise ValueError("图像和标签文件数量不匹配")

    # 创建输出目录
    splits = ['train', 'valid', 'test']
    for split in splits:
        os.makedirs(os.path.join(image_dir, split), exist_ok=True)
        os.makedirs(os.path.join(label_dir, split), exist_ok=True)

    # 验证文件对应关系
    for img, lbl in zip(image_files, label_files):
        if os.path.splitext(img)[0] != os.path.splitext(lbl)[0]:
            raise ValueError(f"文件不匹配: {img} 和 {lbl}")

    # 创建配对列表并打乱
    paired_files = list(zip(image_files, label_files))
    random.shuffle(paired_files)

    # 计算分割点
    total = len(paired_files)
    train_end = int(total * split_ratio[0])
    val_end = train_end + int(total * split_ratio[1])

    # 分割数据集
    train_set = paired_files[:train_end]
    valid_set = paired_files[train_end:val_end]
    test_set = paired_files[val_end:]

    # 复制文件到目标目录
    copy_files(train_set, image_dir, label_dir,
               os.path.join(image_dir, 'train'),
               os.path.join(label_dir, 'train'))

    copy_files(valid_set, image_dir, label_dir,
               os.path.join(image_dir, 'valid'),
               os.path.join(label_dir, 'valid'))

    copy_files(test_set, image_dir, label_dir,
               os.path.join(image_dir, 'test'),
               os.path.join(label_dir, 'test'))

    # 输出统计信息
    print(f"数据集分割完成：")
    print(f"训练集: {len(train_set)} 个样本")
    print(f"验证集: {len(valid_set)} 个样本")
    print(f"测试集: {len(test_set)} 个样本")
