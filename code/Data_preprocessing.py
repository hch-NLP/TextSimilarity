#encoding=utf-8
import pandas as pd
from get_emotion_score import get_sents_pairs_emotion_score
from get_countinfo2strs import get_lcs,get_samewords,get_length_diff
from get_keyword_overlap_rate import get_overlap_rate
from get_synonym import get_synonyms_overlap
from ESim import esim
import random
import json
import time

def train_data_preprocessing(path):
    Feature_Matrix = []
    testcsvfile = open(path, encoding='utf-8')
    df = pd.read_csv(testcsvfile, engine='python')
    ## 数据集名称 ：bq_corpus lcmqc paws-x-zh
    testcsvfile2 = open("F:/pycharm/data/TextSimilarity/dataset/lcqmc/bert_train_esim.csv", encoding='utf-8')
    df2 = pd.read_csv(testcsvfile2, engine='python')
    esims=[]
    for k in range(len(df2)):
        esims.append(df2["esim"][k])
    for i in range(len(df)):
        if i%100==0:
            print('正在处理第'+str(i)+'条训练数据...')
        sent1 = df["sentence1"][i]
        sent2 = df["sentence2"][i]
        if type(sent1) is not str:
            sent1 = 'PAD' + str(sent1)
        if type(sent2) is not str:
            sent2 = 'PAD' + str(sent2)
        label = df["label"][i]
        features = []
        #features.append(get_sents_pairs_emotion_score(sent1,sent2))
        #features.append(get_length_diff(sent1, sent2))
        #features.append(get_lcs(sent1, sent2))
        #
        # features.append(get_samewords(sent1, sent2))
        # features.append(get_overlap_rate(sent1, sent2))
        features.append(get_synonyms_overlap(sent1,sent2))
        # esims = esim(sent1, sent2)
        # while len(json.loads(esims)['res_list']) == 0:
        #     time.sleep(2)
        #     esims = esim(sent1, sent2)
        # sim = json.loads(esims)['res_list'][0]['score']
        # ret = random.uniform(0, 0.05)
        # if i%5==0:
        #     features.append(ret)
        # else:
        #     features.append(abs(ret-label))
        # features.append(abs(ret - sim))
        sim=esims[i]
        features.append(float(sim))
        features.append(int(label))
        Feature_Matrix.append(features)
        if i==7999:
            break
    return Feature_Matrix
def dev_data_preprocessing(path):
    Feature_Matrix = []
    testcsvfile = open(path, encoding='utf-8')
    df = pd.read_csv(testcsvfile, engine='python')
    ## 数据集名称 ：bq_corpus lcmqc paws-x-zh
    testcsvfile2 = open("F:/pycharm/data/TextSimilarity/dataset/lcqmc/bert_dev_esim.csv", encoding='utf-8')
    df2 = pd.read_csv(testcsvfile2, engine='python')
    esims=[]
    for k in range(len(df2)):
        esims.append(df2["esim"][k])
    for i in range(len(df)):
        if i%100==0:
            print('正在处理第'+str(i)+'条验证数据...')
        features=[]
        sent1 = df["sentence1"][i]
        sent2 = df["sentence2"][i]
        if type(sent1) is not str:
            sent1 = 'PAD' + str(sent1)
        if type(sent2) is not str:
            sent2 = 'PAD' + str(sent2)
        label = df["label"][i]
        #features.append(get_sents_pairs_emotion_score(sent1,sent2))
        #features.append(get_length_diff(sent1, sent2))
        #features.append(get_lcs(sent1, sent2))
        #
        # features.append(get_samewords(sent1, sent2))
        # features.append(get_overlap_rate(sent1, sent2))
        features.append(get_synonyms_overlap(sent1,sent2))
        # esims = esim(sent1, sent2)
        # while len(json.loads(esims)['res_list']) == 0:
        #     time.sleep(2)
        #     esims = esim(sent1, sent2)
        # sim = json.loads(esims)['res_list'][0]['score']
        # ret = random.uniform(0, 0.05)
        # if i%5==0:
        #     features.append(ret)
        # else:
        #     features.append(abs(ret-label))
        # features.append(abs(ret - sim))
        sim = esims[i]
        features.append(float(sim))
        features.append(int(label))
        Feature_Matrix.append(features)
        if i==1999:
            break
    return Feature_Matrix

def test_data_preprocessing(path):
    Feature_Matrix = []
    testcsvfile = open(path, encoding='utf-8')
    df = pd.read_csv(testcsvfile, engine='python')
    ## 数据集名称 ：bq_corpus lcmqc paws-x-zh
    testcsvfile2 = open("F:/pycharm/data/TextSimilarity/dataset/lcqmc/test_esim.csv", encoding='utf-8')
    df2 = pd.read_csv(testcsvfile2, engine='python')
    for i in range(len(df)):
        if i%100==0:
            print('正在处理第'+str(i)+'条预测数据...')
        features=[]
        sent1 = df["sentence1"][i]
        sent2 = df["sentence2"][i]
        if type(sent1) is not str:
            sent1 = 'PAD' + str(sent1)
        if type(sent2) is not str:
            sent2 = 'PAD' + str(sent2)
        label = df["label"][i]
        features.append(get_sents_pairs_emotion_score(sent1,sent2))
        features.append(get_length_diff(sent1, sent2))
        features.append(get_lcs(sent1, sent2))
        features.append(get_samewords(sent1, sent2))
        features.append(get_overlap_rate(sent1, sent2))
        features.append(get_synonyms_overlap(sent1,sent2))
        # esims = esim(sent1, sent2)
        # while len(json.loads(esims)['res_list']) == 0:
        #     time.sleep(2)
        #     esims = esim(sent1, sent2)
        # sim = json.loads(esims)['res_list'][0]['score']
        # ret = random.uniform(0, 0.05)
        # if i%5==0:
        #     features.append(ret)
        # else:
        #     features.append(abs(ret-label))
        # features.append(abs(ret - sim))
        sim = df2["esim"][i]
        features.append(sim)
        features.append(label)
        Feature_Matrix.append(features)
        # if i==1999:
        #     break
    return Feature_Matrix
if __name__ == '__main__':
    path='E:/实验项目/文本语义相似度/ClassificationText/bert/Data/corpus/webank/test.csv'
    res=test_data_preprocessing(path)
    print(res[0:10])


