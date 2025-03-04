import os
import argparse

def process_tsv(file_path, old_root_path, new_root_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 处理每一行
    new_lines = []
    for line in lines:
        parts = line.strip().split('\t')
        if parts[0] == '/':  # 第一行替换为新的根目录
            parts[0] = f'{new_root_path}'
            new_lines.append('\t'.join(parts) + '\n')
            continue
        # 替换文件路径为相对路径
        parts[1] = parts[1].replace(old_root_path, '').replace('\\', '/').lstrip('/')
        parts[2] = parts[2].replace(old_root_path, '').replace('\\', '/').lstrip('/')
        new_lines.append('\t'.join(parts) + '\n')
    
    # 保存处理后的文件
    new_file_path = file_path.replace('.tsv', '_m.tsv')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def main(root_path, new_root_path):
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            for file_name in ['train.tsv', 'valid.tsv', 'test.tsv']:
                file_path = os.path.join(dir_path, file_name)
                if os.path.exists(file_path):
                    process_tsv(file_path, root_path, new_root_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process TSV files in subdirectories.')
    parser.add_argument('root_path', type=str, help='The root directory to process')
    parser.add_argument('new_root_path', type=str, help='The new root directory to replace in TSV files')
    args = parser.parse_args()
    
    main(args.root_path, args.new_root_path)