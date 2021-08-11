#encoding=utf-8
import jieba.analyse
def get_overlap_rate(str1,str2):
    sent1=jieba.analyse.extract_tags(str1, topK=5, withWeight=False,allowPOS=('n','nr','nt','ns','nz','v','vn''r'))#,'v','vn'
    sent2=jieba.analyse.extract_tags(str2, topK=5, withWeight=False,allowPOS=('n','nr','nt','ns','nz','v','vn''r'))#,'v','vn'
    count=0.0
    for w1 in sent1:
        for w2 in sent2:
            if w1==w2:
                count=count+1.0
    return count/(min(len(sent1),len(sent2))+0.000000000001)
if __name__ == '__main__':
    s1="一般电话确认要等多久。"
    s2="一般多久才会打电话来"
    print(get_overlap_rate(s1,s2))

