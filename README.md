# spaCyofChinese_ING_202005
用于建立spaCyV2.2 中文语言模型(按文件No序号执行脚本)

1.下载chs-gsd-ud并将其转换为spacy可以读取的json格式文件

2.读取现有的二进制词向量模型（由word2vec训练得到），并且训练spacy词向量管道模型。

3.使用步骤1转换好的文件进行训练，得到spacy tagger,parser管道模型

4.对自己收集到的NER训练语料(CLUENER2020 https://storage.googleapis.com/cluebenchmark/tasks/cluener_public.zip )
  进行转换，转换为可以用于SPACY训练的json格式文件格式，具体格式请参考
  https://github.com/explosion/spacy/blob/master/examples/training/training-data.json

5.使用步骤4得到的json格式文件进行NER管道训练

6.将步骤5与步骤3训练得到的模型进行合并，最后得到包含tagger,parser,ner管道的SPACY模型

PS:我也是初学者，如果有问题请联系QQ517934203 ,如果以上方案有不正确的地方，也请大佬指正。

PS:以上就是训练spacy2.2模型的步骤，其实步骤不是很难，不过目前网上并没有很详细的训练介绍，所以我一开始也捣鼓了半天。

PS:其实训练spacy模型并没有太大的难度，最难的还是对于词向量的训练调整以及语料的收集，笔者步骤4一开始准备使用OntoNotes Release 5.0进行NER模型训练的，
结果由于网站需要加入组织，所以整半天也没有能够将文件下得下来，只好退而求其次随便整了一份NER语料，所以进行步骤4的时候，请大家根据自己语料数据重新编写
py脚本。
