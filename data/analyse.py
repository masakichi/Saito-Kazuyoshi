# coding: utf-8

import csv
from collections import Counter

def main():
    words = {}
    for kind in '副詞,フィラー,助詞,連体詞,接頭詞,動詞,形容詞,助動詞,接続詞,記号,名詞,品詞,感動詞'.split(','):
        words[kind] = []
    with open('./result.csv') as f:
        csv_reader = csv.reader(f)
        csv_reader.next()
        for line in csv_reader:
            if line[2] == '空白':
                continue
            words[line[1]].append(line[-3])
    for k, v in words.iteritems():
        print k
        counter = Counter(v)
        num = 20
        if k in ('動詞,形容詞,名詞'):
            num = 100
        for word, times in counter.most_common(num):
            print word, times
        print '========'

if __name__ == "__main__":
    main()
