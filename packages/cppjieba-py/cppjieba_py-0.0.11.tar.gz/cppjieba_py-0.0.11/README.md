# cppjieba-py   

[![Build Status](https://travis-ci.org/bung87/cppjieba-py.svg?branch=master)](https://travis-ci.org/bung87/cppjieba-py)

cppjieba-py 是 [cppjieba](https://github.com/yanyiwu/cppjieba)的 Python 封装。 

由于只是对cppjieba的接口进行的封装，所以执行效率上非常接近于原cppjieba。  

项目主要分为两个部分**libcppjieba** 为 cppjieba 的 python extension，  
**cppjieba_py** 为使开发者平滑过渡到使用cppjieba-py而作的 python package。 
具体见[example.py](example.py)。  

### 区别  

* 原jieba的`.cut`族接口基本都由python的`iter()`函数包裹list结果来实现。  
* 原jieba的`.set_*`方法基本都由class传入初始化的参数来完成。   
* `.del_word` 和`.suggest_freq` cppjieba没提供。  
* `POSTokenizer.lcut` 在`Tokenizer.tag` 下， 唯一一个只提供了list返回类型的接口。

## 安装  

* pypi  

	```pip install cppjieba-py```  
	
	或者你设置的安装源并未收录本项目  

	```pip install -i https://pypi.org/simple/ cppjieba-py```  

* 从发行包安装  
	see [releases](https://github.com/bung87/cppjieba-py/releases)  

	```pip install https://github.com/bung87/cppjieba-py/files/<xxxxxxx>/cppjieba_py-<x.x.x>.tar.gz```  

* 从源代码安装

	```
	$ git clone --recursive https://github.com/bung87/cppjieba-py
	$ python setup.py install 
	```


## 使用

下面是一个使用 cppjieba-py 进行分词的例子

```python
# -*- coding: utf-8 -*-
import cppjieba_py as jieba 
# or use defualt Tokenizer: jieba.cut 
jieba_instance = Tokenizer()
seg_list = jieba_instance.cut("我来到北京清华大学",cut_all = True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式


seg_list = jieba_instance.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba_instance.cut_for_search(
    "小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))
    
```

for more: [example.py](example.py) , [tests](tests)

## 性能  

[performace_test/speed.py](performace_test/speed.py)  

测试[方案](https://yanyiwu.com/work/2015/06/14/jieba-series-performance-test.html)：先按行读取文本围城到一个数组里，然后循环对围城每行文字作为一个句子进行分词。因为只对围城这本书分词一遍太快了，容易误差。 所以循环对围城这本书分词50次。基本上每次分词耗时都很稳定。 分词算法都是采用【精确模式】。

`lcut HMM=False`  

| 方案        | 速度             |
| ------------- |:-------------:|
| cppjieba-py      | 10.642102  |
| jieba-fast==0.51      | 26.129298  |
| jieba==0.39      | 50.623866    |

`lcut HMM=True`  

| 方案        | 速度             |
| ------------- |:-------------:|
| cppjieba-py      | 13.139232  |
| jieba-fast==0.51      | 34.574907  |
| jieba==0.39      | 1:26.756226    |

`posseg.lcut`   

| 方案        | 速度             |
| ------------- |:-------------:|
| cppjieba-py      | 20.382905  |
| jieba==0.39    | 1:19.411649    |

## Test  

`pip install ".[test]"`  
`nosetests -c nose.cfg`