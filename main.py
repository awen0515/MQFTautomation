import os
import datetime
import pandas as pd
from tqdm import tqdm
import xlwt
from collections import Counter
from log_files import create_log_files
from target_words import create_target_words


# 日志文件夹的路径
log_folder = r'D:\日志'

# 获取当前日期
current_date = datetime.date.today().strftime('%Y-%m-%d')

# 定义剪切图文件夹路径
source_folder = r"D:\剪切图"

# 定义目标文件夹路径
destination_folder = r"D:\日志"

# 获取剪切图文件夹中的所有子文件夹
subfolders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]

# 遍历子文件夹列表
for folder_name in subfolders:
    # # 检查文件夹名称是否包含"模切背光"或"模切线扫"
    # if "模切背光" in folder_name or "模切线扫" in folder_name or "1" in folder_name or "2" in folder_name or "3" in folder_name:
    # 生成日志文件夹名
    log_folder_name = folder_name + "未达标日志"

    # 生成日志文件名
    log_file_name = folder_name + "_" + current_date + ".log"

    # 创建日志文件夹的完整路径
    log_folder_path = os.path.join(log_folder, log_folder_name)

    # 创建日志文件夹
    os.makedirs(log_folder_path, exist_ok=True)

    # 生成日志文件路径
    log_file_path = os.path.join(log_folder_path, log_file_name)

    # 创建并写入日志文件
    with open(log_file_path, 'w') as log_file:
        # log_file.write("这是 {} 的未达标日志".format(folder_name))
        log_file.write(format(""))

        #获取未达标文件夹路径
        folder_path = os.path.join(source_folder, folder_name, "未达标")

         # 检查未达标文件是否存在
        if os.path.exists(folder_path)and os.path.isdir(folder_path):
            # 遍历未达标文件夹下的所有文件
            files = os.listdir(folder_path)
            for file in files:
                # 写入日志文件
                log_file.write(file + "\n")
        else:
            log_file.write("未达标文件不存在\n")

    print("生成日志文件夹：{}".format(log_folder_path))

# 创建字典的简化方式
log_files = create_log_files()
target_words = create_target_words()

# 创建一个空的DataFrame
result_df = pd.DataFrame(columns=['日志类型', '词汇', '数量'])

# 创建日志统计文件路径
log_stats_file = os.path.join(log_folder, f'日志统计文件_{current_date}.txt')

# 遍历处理每个日志类型和对应的日志文件。
for log_type, file_name in log_files.items():
    # 将日志文件夹路径、日志类型文件夹和日志文件名连接起来。
    log_file_path = os.path.join(log_folder, log_type, file_name)

    # 判断文件是否存在
    if os.path.exists(log_file_path):
        print(f"在路径 '{os.path.join(log_folder, log_type)}' 下，文件 '{file_name}' 存在")
        with open(log_stats_file, 'a') as stats_file:
            stats_file.write(f"在路径 '{os.path.join(log_folder, log_type)}' 下，文件 '{file_name}' 存在\n")

        # 存储每个词汇的数量统计，初始值都为 0。
        word_count = {word: 0 for word in target_words[log_type]}
        # 打开日志文件，encoding='gbk'为编码格式
        # 在文件的每一行中，我们遍历 target_words 列表，并判断每个词汇是否在当前行中出现。
        # 如果出现，我们将对应词汇在 word_count 字典中的值加 1。
        with open(log_file_path, 'r', encoding='gbk') as file:
            for line in file:
                for word in target_words[log_type]:
                    if word in line:
                        word_count[word] += 1
        # 统计词汇数量放下方，注意注意注意，解开此封印会导致程序多次统计
        # tqdm.write(f"词汇 '{word}' 的数量：{word_count[word]}")
        # with open(log_stats_file, 'a') as stats_file:
        #     stats_file.write(f"词汇 '{word}' 的数量：{word_count[word]}\n")

        # 创建一个临时DataFrame，用于存储当前日志类型的统计结果
        temp_df = pd.DataFrame({'日志类型': log_type, '词汇': list(word_count.keys()), '数量': list(word_count.values())})

        for word, count in word_count.items():
            print(f"词汇 '{word}' 的数量：{count}")
            with open(log_stats_file, 'a') as stats_file:
                stats_file.write(f"词汇 '{word}' 的数量：{count}\n")

        # 将临时DataFrame添加到结果DataFrame中
        result_df = pd.concat([result_df, temp_df], ignore_index=True)

    else:
        print(f"在路径 '{os.path.join(log_folder, log_type)}' 下，文件 '{file_name}' 不存在")
        with open(log_stats_file, 'a') as stats_file:
            stats_file.write(f"在路径 '{os.path.join(log_folder, log_type)}' 下，文件 '{file_name}' 不存在\n")

# # 将结果保存到Excel文件中
# excel_path = os.path.join(log_folder, '日志统计.xls')
# result_df.to_excel(excel_path, index=False)
# print(f"结果已保存到Excel文件：{excel_path}")
