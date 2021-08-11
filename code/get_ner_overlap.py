# -*- coding: utf8 -*-
import json
import http.client
# 其中，input_spec表示输入的语言种类，它有三个取值，分别是自动识别语言(“auto”)，中文（“chs”）和英文（“en”）。”enable”可以取”true”或”false”,表示是否要激活对应的功能。”alg”表示对应的功能需要调用什么算法，”pos_tagging”中的”alg”有三种选择(“crf”, “dnn”, “log_linear”)， ”ner“中的”alg”有两种选择(“crf“和”dnn”)。”fine_grained”表示是否要返回细粒度NER的结果。”echo_data“的取值由用户自由定义，用户可以用它来记录当前request的标识信息，如request_id，它在异步调用等场合可能会有用。
# 批处理调用
# Texsmart支持批处理调用API：通过一个JSON输入，处理多个（中文和英文）句子的分析。它的JSON输入实例如下：
#
# {
#   "str":[
#          "上个月30号，南昌王先生在自己家里边看流浪地球边吃煲仔饭。",
#          "2020年2月7日，经中央批准，国家监察委员会决定派出调查组赴湖北省武汉市，就群众反映的涉及李文亮医生的有关问题作全面调查。",
#          "John Smith stayed in San Francisco last month."
#         ]
# }
# 请注意，批处理调用的输出格式跟普通调用的输出格式有一些区别，所有句子的分析结果构成一个JSON array，作为"res_list"字段的值。

def get_ners(sentence):
    obj = {"str": sentence,
           "options":
               {
                   "input_spec": {"lang": "auto"},
                   "word_seg": {"enable": True},
                   "pos_tagging": {"enable": True, "alg": "log_linear"},#“crf”, “dnn”, “log_linear”
                   "ner": {"enable": True, "alg": "fine.std"},#(“crf“和”dnn”) fine.std
                   "syntactic_parsing": {"enable": True},
                   "srl": {"enable": True},
                   "text_cat": {"enable": True},
               },
           "echo_data": {"API_test": 101}
           }
    req_str = json.dumps(obj)
    conn = http.client.HTTPSConnection("texsmart.qq.com")
    conn.request("POST", "/api", req_str)
    response = conn.getresponse()
    #print(response.status, response.reason)
    res_str = response.read().decode('utf-8')
    #print(res_str)
    res=json.loads(res_str)
    for i in range(len(res['entity_list'])):
        print(res['entity_list'][i]['str'])
        print(res['entity_list'][i]['type']['i18n'])
    print(res['syntactic_parsing_str'])

if __name__ == '__main__':
    sentence='他在看流浪地球和中国好声音。'
    get_ners(sentence)