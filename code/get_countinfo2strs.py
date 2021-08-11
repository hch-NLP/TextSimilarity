#encoding=utf-8
#最长公共子序列
import jieba
def get_lcs(str1,str2):
    matrix = []
    xmax = 0
    xindex = 0
    for i, x in enumerate(str2):
        matrix.append([])
        for j, y in enumerate(str1):
            if x != y:
                matrix[i].append(0)
            else:
                if i == 0 or j == 0:
                    matrix[i].append(1)
                else:
                    matrix[i].append(matrix[i - 1][j - 1] + 1)
                if matrix[i][j] > xmax:
                    xmax = matrix[i][j]
                    xindex = j
                    xindex += 1
    return len(str1[xindex - xmax: xindex])/(min(len(str1),len(str2))+0.0000000000001)
# 查找两个字符串中所有相同字符
def get_samewords(str1,str2):
    res = []
    seg1 = jieba.lcut(str1, cut_all=False)
    seg2 = jieba.lcut(str2, cut_all=False)
    for x in seg1:
        if x in seg2:
            res.append(x)
    return len(res)/(min(len(seg1),len(seg2))+0.000000000000001)
#计算句子之间长度差的比率
def get_length_diff(str1,str2):
    return abs(len(str1)-len(str2))/(max(len(str1),len(str2))+0.0000000000001)
if __name__ == '__main__':
    s1 = '一般电话确认要等多久。'
    s2 = '一般多久才会打电话来'
    print(get_lcs(s1, s2))
    print(get_samewords(s1, s2))
    print(get_length_diff(s1,s2))