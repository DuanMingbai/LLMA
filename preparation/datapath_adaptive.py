import os
import argparse
from tqdm import tqdm

def process_tsv_file(tsv_path, old_root_path, new_root_path):
    with open(tsv_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 替换第一行为 new_root_path
    lines[0] = new_root_path + '\n'

    # 统一将路径中的反斜杠替换为正斜杠
    old_root_path = old_root_path.replace('\\', '/')

    # 处理剩余行
    for i in range(1, len(lines)):
        # 统一将行中的反斜杠替换为正斜杠
        lines[i] = lines[i].replace('\\', '/')
        parts = lines[i].strip().split()
        if len(parts) >= 3:  # 确保每行至少有 3 个部分
            # 替换 parts[1] 和 parts[2] 中的 old_root_path
            parts[1] = parts[1].replace(old_root_path, '').lstrip('/')
            parts[2] = parts[2].replace(old_root_path, '').lstrip('/')
            lines[i] = '\t'.join(parts) + '\n'

    # 保存处理后的文件
    new_tsv_path = tsv_path.replace('.tsv', '_m.tsv')
    with open(new_tsv_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def main(old_root_path, new_root_path, real_root_path):
    # 遍历 real_root_path 下的所有子文件夹
    subdirs = [os.path.join(real_root_path, d) for d in os.listdir(real_root_path) if os.path.isdir(os.path.join(real_root_path, d))]
    
    # 使用 tqdm 显示进度条
    for subdir in tqdm(subdirs, desc="Processing directories"):
        # 遍历子文件夹中的 train.tsv, valid.tsv, test.tsv
        for tsv_file in ['train.tsv', 'valid.tsv', 'test.tsv']:
            tsv_path = os.path.join(subdir, tsv_file)
            if os.path.exists(tsv_path):
                process_tsv_file(tsv_path, old_root_path, new_root_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process TSV files.")
    parser.add_argument('old_root_path', type=str, help='The old root path to be replaced.')
    parser.add_argument('new_root_path', type=str, help='The new root path to replace the old one.')
    parser.add_argument('real_root_path', type=str, help='The real root path containing subdirectories with TSV files.')

    args = parser.parse_args()

    main(args.old_root_path, args.new_root_path, args.real_root_path)