# -*- coding: utf-8 -*-

import os
import inspect
import pandas as pd
import nltk
import pickle
import joblib
import ease.external_code.dataAumentationByTranslation
#from ease import util_functions
from ease.create import create
from ease import util_functions
# training_set_rel3.xlsx 를 현재 디렉토리로 옮겨야됨
#논술 한글
testSet = pd.read_csv("ebsi_0701_testset.csv")
trainSet = pd.read_csv("ebsi_0701_trainset.csv")
df = trainSet["score"].value_counts()
print(250//df[4])

#한글 ASAP
#df = pd.read_csv("training_set_rel3_ko.tsv")

# df = df[df['essay_set']==1]
# df['score'] = df['domain1_score']
#df = pd.read_csv('/Users/hwangyun/PycharmProjects/ease_real/testfile.csv')

#"짝수" if num % 2 == 0 else "홀수"
#df['score']
#df = df[['essay_ko', "score"]]

# df["domain1_score"] = df["domain1_score"].astype(int)

prompt = """제시문 (가)와 제시문 (나)의 ‘경쟁’에 대한 견해를 비교하시오.
(가) 인간을 공격적이고 이기적인 존재로 보았던 영국의 철학자 토머스 홉스 역시 경쟁심은 인간 의 본능이라고 말했습니다. 인간의 본성 중에는 싸움을 불러일으키는 세 가지 요소인 경쟁심, 소 심함, 명예욕이 있는데, 특히 경쟁심은 인간이 필요한 무엇인가를 얻기 위해 다른 사람과 투쟁하 도록 만든다는 것입니다. 이런 점들로 보아, 경쟁은 우리 삶에서 떼어 낼 수 없는 불가피한 것입 니다. 따라서 우리에게는 경쟁을 부정하는 것이 아니라, 경쟁의 긍정적인 힘을 배우고 활용하는 지혜가 필요합니다. 그럼에도 불구하고 경쟁 그 자체를 부정하거나 경쟁 논리라면 무조건 반대하는 사람들이 있습 니다. 이들은 경쟁이 서로를 적대시하게 만들어 인간관계를 해친다고 비판합니다. 효율성과 적자 생존의 법칙을 앞세운 경쟁 논리는 경쟁에서 탈락한 사람들을 도외시한 채, 결국 강자의 이익만 을 대변한다는 것입니다. 그러나 이는 경쟁에 대한 오해입니다. 경쟁은 경쟁자를 부정하고 배제 하는 것이 아니라, 서로를 인정하고 그 바탕 위에서 각자의 의욕과 노력을 한층 더 이끌어 내는 긍정적 상호작용이라 할 수 있습니다. 요즘 사회를 가리켜 유독 ‘경쟁 사회’라 부르며, 승자와 패자를 가혹하게 가르는 약육강식의 비 정함을 비난하는 사람들이 있습니다. 하지만 잘 생각해 보면, 동서고금을 막론하고 인간 사회가 경쟁 사회가 아니었던 적은 찾아보기가 어렵습니다. 우리 사회에서 경쟁은 앞으로도 계속될 것입 니다. 따라서 앞으로의 과제는 경쟁할 것인가 말 것인가를 선택하는 일이 아니라, 공정한 경쟁을 추구하기 위한 방식에 대한 고민을 함께하는 것입니다.
(나) 사람들은 흔히 인간 사회에서 나타나는 경쟁 구도를 설명할 때 찰스 다윈의 ‘진화론’을 언급 하고는 한다. 세상에 존재하는 모든 부조리와 불평등의 근원은 약육강식과 적자생존의 원리이고, 진화론은 이를 잘 뒷받침해 주는 논리라고 생각한다. 하지만 과연 그럴까? 사실, 진화론만큼 많 은 오해를 받은 과학 이론도 드물다. 다윈이 주목한 지점은 생물체에 일어나는 ‘변이의 다양성’이었다. 다윈은 이러한 변이가 쌓여 점 차 환경에 더 잘 적응된 방식으로 변화한다고 생각했다. 하지만 ‘더 잘 적응한 방식’이 오로지 ‘한 가지 방식’뿐이라고 말한 적은 없다. 오히려 자연 선택의 다양성에 대해 더 많은 주의를 기울 였다. 좀 더 구체적으로 말하자면, 다윈은 “변화는 생명체가 환경에 더욱 잘 적응하기 위해서, 번식 행위를 통해 우연히 이루어진다. 그 과정에 어떤 외부의 힘이 개입하여 작용하지 않으며, 모든 생명체는 우열이 없다.”라고 썼다. 이 글 어디에서도 약한 것이 강한 것보다 열등하며, 강 자가 약자를 짓밟아도 좋다는 뜻은 담겨 있지 않다. 다윈은 다양한 생물 종을 관찰한 뒤, 생물체 를 있게 한 원동력은 환경에 적응하며 얻게 된 ‘다양성’이라는 결론을 내렸다. 다양한 생물 종이 아무리 제각각 다양한 자원을 나누며 살아간다고 해도, 생물의 가짓수에 비 해 자원의 가짓수는 적을 수밖에 없다. 따라서 같은 자원을 놓고 여러 생물 종이 경쟁해야 하는 일은 피할 수 없다. 그러나 실제로 많은 생물 종은 서로를 내쫓기 위해 싸움을 벌이기보다는 서 로 공존하는 방식을 찾고는 한다. 이러한 다양한 예를 들며 실제로 경쟁보다는 공생이 진화의 원동력이라고 주장하는 학자도 많다. 여성 생물학자 린 마굴리스는 공생 진화론을 주장하는 학자의 한 사람이다. 공생 진화론에 따르면, 생명체는 한정된 자원을 놓고 서로 경쟁하기보다는 한발 물러서서 상부상조 전략을 추구한다. 지의류는 잘 알려진 공생 생물이다. 얼핏 보기에는 이끼처 럼 보이는 지의류는 사실 곰팡이나 버섯 같은 균류와 파래나 청각 같은 조류가 한데 어우러진 생물체다. 지의류의 공생 관계는 너무도 밀접하여 이 둘을 분리하면 단독 생활을 할 수 없을 정 도로 서로에 대한 의존도가 강하다. 지의류는 균류와 조류가 합쳐서 진화한 새로운 생물 종이라 고 생각될 정도이다. 이처럼 진화론은 태생부터 경쟁보다는 공존의 논리에 바탕을 두고 있었는데, 우리는 오래도록 이를 알아차리지 못하는 실수를 저질렀다. 하지만 이제 세상은 변하고 있다. 획일성과 경쟁, 반 목과 전쟁이 난무하던 시대는 가고, 다양성과 화합, 공존과 더불어 사는 삶이 최대의 가치가 되 는 시대가 오고 있다.
"""



essays = trainSet["essay"].tolist()
scores = trainSet["score"].tolist()
model = create(essays, scores, prompt)
# joblib.dump(model, 'model.pkl')
# model = joblib.load('model.pkl')
for key, value in model.items():
  if key != "text" and key != "score" and key != "prompt":
    print(key,":",value)


from ease.grade import grade



predList = []
for data in testSet["essay"]:
  score = grade(model, data)
  predList.append(score["score"])
  print(score)
  print("당신의 점수는", score["score"], "점입니다.")

print("kappa_score:", util_functions.quadratic_weighted_kappa(predList, list(testSet["score"])))
print()
print(predList)
print(list(testSet["score"]))