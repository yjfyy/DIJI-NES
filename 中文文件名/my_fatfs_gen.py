#!/usr/bin/env python
import os
import sys
import subprocess
import shutil
import tempfile

# 创建临时目录，用 ASCII 文件名代替中文名
temp_dir = tempfile.mkdtemp()

# 复制文件并重命名为 ASCII 名称
source_dir = r'D:\github\public\DIJI-NES\data'
name_mapping = {}

for filename in os.listdir(source_dir):
    if os.path.isfile(os.path.join(source_dir, filename)):
        # 生成 ASCII 短文件名（保留原始文件名用于后续映射）
        ascii_name = f"FILE_{len(name_mapping):04d}.nes"
        shutil.copy2(os.path.join(source_dir, filename), 
                     os.path.join(temp_dir, ascii_name))
        name_mapping[ascii_name] = filename

# 调用 fatfsgen.py
fatfsgen_path = r'C:\Espressif\frameworks\esp-idf-v5.5.5\components\fatfs\fatfsgen.py'
args = [
    sys.executable,
    fatfsgen_path,
    temp_dir,
    '--output_file', 'fatfs.bin',
    '--partition_size', '0x100000',
    '--long_name_support'
]

subprocess.run(args)

# 清理临时目录
shutil.rmtree(temp_dir)

print("生成的 fatfs.bin 包含以下文件映射：")
for ascii_name, real_name in name_mapping.items():
    print(f"  {ascii_name} -> {real_name}")