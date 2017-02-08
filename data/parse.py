# coding: utf-8

import glob
import os
import MeCab
import csv

mecab = MeCab.Tagger()

def main():
    dirname =  os.path.dirname(os.path.abspath(__file__))
    print dirname
    paths = glob.glob('%s/*/*.txt' % dirname)
    uniq_paths = []
    pool = set()
    for path in paths:
        _, filename = os.path.split(path)
        if filename in pool:
            continue
        uniq_paths.append(path)
        pool.add(filename)

    print len(paths), len(uniq_paths)
    with open('result.csv', 'w') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow('表層形,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音'.split(','))
        for path in uniq_paths:
            with open(path) as f:
                for line in f:
                    line = line.strip('\n')
                    if not line:
                        continue
                    rows = parse(line)
                    csv_writer.writerows(rows)
            print '%s finished.' % path

def parse(text):
    result = mecab.parse(text)
    rows = []
    for line in result.split('\n'):
        if not line.strip():
            continue
        if line == 'EOS':
            break
        word, info = line.split('\t')
        rows.append([word]+info.split(','))
    return rows
        

if __name__ == "__main__":
    main()
