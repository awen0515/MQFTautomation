# log_files.py

import datetime

def create_log_files():
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    log_files = {
        '报警日志': f'报警日志_{current_date}.log',
        '打标日志': f'打标日志_{current_date}.log',
        '纠偏日志': f'纠偏日志_{current_date}.log',
        '算法日志': f'算法日志_{current_date}.log',
        '通讯日志': f'通讯日志_{current_date}.log',
        '运行日志': f'运行日志_{current_date}.log',
        '修改日志': f'修改日志_{current_date}.log',
    }
    return log_files
