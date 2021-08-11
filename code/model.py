#encoding=utf-8
import pickle
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import naive_bayes
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import  AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import classification_report
from Data_preprocessing import train_data_preprocessing,test_data_preprocessing,dev_data_preprocessing
import time
def train():
    # train_data = 'E:/实验项目/文本语义相似度/ClassificationText/bert/Data/corpus/webank/train.csv'
    # test_data = 'E:/实验项目/文本语义相似度/ClassificationText/bert/Data/corpus/webank/dev.csv'
    ## 数据集名称 ：bq_corpus lcmqc paws-x-zh
    train_data = 'F:/pycharm/data/TextSimilarity/dataset/lcqmc/train.csv'
    test_data = 'F:/pycharm/data/TextSimilarity/dataset/lcqmc/dev.csv'

    train_x = []
    train_y = []
    test_x = []
    test_y = []
    print('正在处理训练数据...')
    train = train_data_preprocessing(train_data)
    print('正在处理验证数据...')
    test = dev_data_preprocessing(test_data)
    for data in train:
        train_x.append(data[0:-1])
        train_y.append(data[-1])
    for data in test:
        test_x.append(data[0:-1])
        test_y.append(data[-1])
    print('数据处理已完成...')
    print(train_x[0:10])
    print(test_x[0:10])
    print('正在训练模型...')
    SVM_MODEL = naive_bayes.GaussianNB().fit(train_x, train_y)
    #SVM_MODEL = LogisticRegression(max_iter=100,penalty='l2',C=0.6).fit(train_x, train_y)
    #SVM_MODEL = KNeighborsClassifier(n_neighbors=50).fit(train_x, train_y)
    #SVM_MODEL = tree.DecisionTreeClassifier(max_depth=3).fit(train_x, train_y)
    #SVM_MODEL  = GradientBoostingClassifier(n_estimators=50).fit(train_x, train_y)
    #SVM_MODEL  = AdaBoostClassifier(n_estimators=50).fit(train_x, train_y)
    #SVM_MODEL = SVC(kernel='linear', C=0.8).fit(train_x, train_y)#kernel='linear', C=0.2 kernel='rbf', C=0.1 kernel='sigmoid', C=0.4
    #SVM_MODEL = RandomForestClassifier(max_depth=30, n_estimators=100,random_state=5).fit(train_x, train_y)
    # 保存训练好的模型
    print('正在保存训练好的模型...')
    s = pickle.dumps(SVM_MODEL)
    f = open('F:/pycharm/data/TextSimilarity/model/lcqmc_svm.model', "wb+")
    f.write(s)
    f.close()
    print('模型训练已完成...')
    pred_y = SVM_MODEL.predict(test_x)
    # pred_y =[]
    # for x in test_x:
    #     if x[0] >= 0.95:
    #         pred_y.append([1])
    #     else:
    #         pred_y.append([0])
    print('直接预测结果')
    print(classification_report(test_y, pred_y))
    score_lr = metrics.accuracy_score(test_y, pred_y)  # 模型准确率
    print('Avg Accuracy: ',score_lr)

def predict():
    pred_x=[]
    pred_data = 'F:/pycharm/data/TextSimilarity/dataset/lcqmc/test.csv'
    print('正在处理预测数据...')
    pred = test_data_preprocessing(path=pred_data)
    for data in pred:
        pred_x.append(data[0:-1])
    # 加载训练好的模型进行预测
    print('正在加载训练好的模型...')
    f2 = open('F:/pycharm/data/TextSimilarity/model/lcqmc_rf.model', 'rb')
    s2 = f2.read()
    svm_model = pickle.loads(s2)
    print('模型加载完成...')
    pred_y = svm_model.predict(pred_x)
    print('加载模型得到的预测结果...')
    print(pred_y[0:10])
    with open("C:/Users/lenovo/Desktop/lcqmc.tsv", "w") as f:
        f.write('index' + '\t' + 'prediction' + '\n')
        for index in range(len(pred_y)):
            f.write(str(index) + '\t' + str(pred_y[index]) + '\n')
            f.flush()
        f.close()
if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
    train()
    print(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
    # predict()