import os

original_file_path = 'data/词性标注@人民日报199801.txt'


if __name__ == '__main__':
    with open('test_text', 'wt', encoding='utf-8') as w:
        with open(original_file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                line_list = line.split()[1:]
                word_list = [item.split('/')[0] for item in line_list]
                line_str = '  '.join(word_list) + '\n'
                w.write(line_str)
                