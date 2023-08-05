import os
import re
from .config import hmm_model_dir, pos_tagging_data_dir, cut_data_dir


def pos2cut_people_daily(pos_file_path, cut_file_path):
    with open(pos_file_path, 'rt', encoding='utf-8') as f:
        with open(cut_file_path, 'wt', encoding='utf-8') as q:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                _, text = line.split(maxsplit=1)  # 去除前面的时间
                text = re.sub(r'\[|/\w*|]\w*', '',
                              text)  # 这一步可以把 复合词性 和 普通词性 全部去掉
                q.write(text + '\n')


if __name__ == '__main__':
    pos_file_path = os.path.join(pos_tagging_data_dir,
                                 "POS tagging@People's Daily199801")
    cut_file_path = os.path.join(cut_data_dir, "CUT@People's Daily199801")
    pos2cut_people_daily(pos_file_path, cut_file_path)
    pass
