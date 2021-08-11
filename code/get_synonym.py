#encoding=utf-8
import codecs
import jieba
path='F:/pycharm/data/TextSimilarity/dict/synonym/同义词库.txt'
def construction_wordpairs(filepath):
    wordpairs={}
    with codecs.open(filepath, mode='r', encoding='utf8') as fr:
        lines = fr.readlines()
        for line in lines:
            if '=' in line:
                s=line.replace('\n','').split('= ')[1]
                w=s.split(' ')
                for i in range(0,len(w)):
                    tmp=[]
                    for word in w:
                        if word != w[i] and len(word)>1:
                            tmp.append(word)
                    wordpairs[w[i]]=tmp
            if '#' in line:
                s = line.replace('\n','').split('# ')[1]
                w = s.split(' ')
                for i in range(0,len(w)):
                    tmp=[]
                    for word in w:
                        if word != w[i] and len(word)>1:
                            tmp.append(word)
                    wordpairs[w[i]]=tmp
    return wordpairs
dic = construction_wordpairs(path)
def get_cilinsynonyms(word):
    return dic.get(word)
def get_synonyms_overlap(sent1,sent2):
    seg1 = jieba.analyse.extract_tags(sent1, topK=3, withWeight=False,allowPOS=('n','nr','nt','ns','nz','v','vn''r'))
    seg2 = jieba.analyse.extract_tags(sent2, topK=3, withWeight=False,allowPOS=('n','nr','nt','ns','nz','v','vn''r'))
    s1=set()
    s2=set()
    for word in seg1:
        words=get_cilinsynonyms(word=word)
        if words is None:
            return 0.0
        else:
            for w in words:
                s1.add(w)
                s1.add(word)
    for word in seg2:
         s2.add(word)
    res=s1.intersection(s2)
    if len(res)>0:
        return len(res)/(min(len(seg1),len(seg2))+0.00000000001)
    else:
        return 0.0


if __name__ == '__main__':
    print(get_cilinsynonyms(word='手机号'))