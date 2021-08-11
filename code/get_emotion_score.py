#encoding=utf-8
import jieba
import pandas as pd


# 载入情感词典
# 打开词典文件，返回列表
def open_dict(Dict='情感词典', path='F:/pycharm/data/TextSimilarity/dict/emotion_dict/'):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r', encoding='utf-8-sig', errors='ignore')  # encoding='utf-8-sig',检查是否有文件头，并去掉
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        word = word.strip(' ')
        dict.append(word)
    return dict


posdict = open_dict(Dict='posdict')  # 积极情感词典
negdict = open_dict(Dict='negdict')  # 消极情感词典
inversedict = open_dict(Dict='inversedict')
mostdict = open_dict(Dict='mostdict')
verydict = open_dict(Dict='verydict')
moredict = open_dict(Dict='moredict')
ishdict = open_dict(Dict='ishdict')
insufficientdict = open_dict(Dict='insufficientdict')
stopwords = open_dict(Dict='stopword')

f = open('F:/pycharm/data/TextSimilarity/dict/emotion_dict/酒店情感词典.txt', 'r', encoding='utf-8')
words = []
value = []
for word in f.readlines():
    words.append(word.split(' ')[0])
    value.append(float(word.split(' ')[1].strip('\n')))

c = {'words': words,
     'value': value}
fd = pd.DataFrame(c)
pos = fd['words'][fd.value > 0]
posdict = posdict + list(pos)  ##加入酒店相关的正向情感词
neg = fd['words'][fd.value < 0]
negdict = negdict + list(neg)  ##加入酒店相关的负向情感词
f.close()


# 分句
def cut_sentence(words):
    start = 0
    i = 0
    sents = []
    token = []
    punt_list = ';；!?。！？'
    if type(words) is not str:
        words = 'PAD' + str(words)
    for word in words:
        if word in punt_list:  # 检查标点符号下一个字符是否还是标点
            sents.append(words[start:i + 1])
            start = i + 1
            i += 1
        else:
            i += 1
            token = list(words[start:i + 2]).pop()  # 取下一个字符
    if start < len(words):
        sents.append(words[start:])
    return sents


# 定义判断奇偶的函数
def judgeodd(num):
    if num % 2 == 0:
        return 'even'
    else:
        return 'odd'


# 计算正、负和总的情感得分
def sentiment(review):
    sents = cut_sentence(review)
    pos_senti = 0  # 段落的情感得分
    neg_senti = 0
    total_senti = 0
    for sent in sents:
        pos_count = 0  # 句子的情感得分
        neg_count = 0
        seg = jieba.lcut(sent, cut_all=False)
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        poscount = 0  # 正向词的第一次分值
        poscount2 = 0  # 正向词反转后的分值
        poscount3 = 0  # 正向词的最后分值
        negcount = 0  # 负向词的第一次分值
        negcount2 = 0  # 负向词反转后的分值
        negcount3 = 0  # 负向词的最后分值
        for word in seg:
            poscount = 0
            negcount = 0
            if word in stopwords:
                pass
            elif word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0  # 情感词前否定词的个数
                for w in seg[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount /= 2.0
                    elif w in insufficientdict:
                        poscount /= 4.0
                    elif w in inversedict:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化
            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in seg[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount /= 2.0
                    elif w in insufficientdict:
                        negcount /= 4.0
                    elif w in inversedict:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            i += 1  # 扫描词位置前移
        if poscount3 < 0 and negcount3 >= 0:
            neg_count += negcount3 - poscount3
            pos_count = 0
        elif negcount3 < 0 and poscount3 >= 0:
            pos_count = poscount3 - negcount3
            neg_count = 0
        elif poscount3 < 0 and negcount3 < 0:
            neg_count = -poscount3
            pos_count = -negcount3
        else:
            pos_count = poscount3
            neg_count = negcount3
        pos_senti = pos_senti + pos_count
        neg_senti = neg_senti + neg_count
    total_senti = pos_senti - neg_senti
    return total_senti
    # if total_senti > 0:
    #     return 1
    # elif total_senti == 0:
    #     return 0
    # else:
    #     return -1

def get_sents_pairs_emotion_score(sent1,sent2):
    if sentiment(sent1)*sentiment(sent2)>=0:
        return abs(abs(sentiment(sent1))-abs(sentiment(sent2)))
    else:
        return abs(sentiment(sent1)) + abs(sentiment(sent2))
    # if abs(sentiment(sent1)-sentiment(sent2))>0:
    #     return 0.0
    # else:
    #     return 1.0
if __name__ == '__main__':
    sent1='设计大方'
    sent2='不过拍照有点差'
    print('情感一致性为：',get_sents_pairs_emotion_score(sent1,sent2))
    review='服务态度极其差，前台接待好象没有受过培训，连基本的礼貌都不懂，竟然同时接待几个客人。'
    print('情感得分为：',sentiment(review))

