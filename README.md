# customize-json-dumps

These tests are originated from http://stackoverflow.com/questions/13249415/

`test3()` is an right answer, while `test1()` is a wrong answer.

`test6()` is based on `test3()` and be modified to automatically wrap list element

=======

心得：

只有 json.dumps 不認識的 class object 才會被丟到自定義的 `cls` 或 `default` function

認不認識可參考：https://docs.python.org/2/library/json.html#encoders-and-decoders

在 `test3()` 作法裡，`default` 處理不了的就丟給 super 的意義在於，要是有其他種奇怪的物件，我們自定義的 Encoder 處理不了的，應該要交給上層去 raise exception。

=======

example output:

```
----------------------test1-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": "[{'y': 7, 'x': 1}, {'y': 4, 'x': 0}, {'y': 3, 'x': 5}, {'y': 9, 'x': 6}]"
    }
  }
}
Check: False

----------------------test2-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": "[{'y': 7, 'x': 1}, {'y': 4, 'x': 0}, {'y': 3, 'x': 5}, {'y': 9, 'x': 6}]"
    }
  }
}
Check: False

----------------------test3-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": [{"y": 7, "x": 1}, {"y": 4, "x": 0}, {"y": 3, "x": 5}, {"y": 9, "x": 6}]
    }
  }
}
Check: True

----------------------test4-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": "@@8bb089f7812049bf994d4e038ee28588@@"
    }
  }
}
Check: False

----------------------test5-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": [
  {
    "y": 7, 
    "x": 1
  }, 
  {
    "y": 4, 
    "x": 0
  }, 
  {
    "y": 3, 
    "x": 5
  }, 
  {
    "y": 9, 
    "x": 6
  }
]
    }
  }
}
Check: True

----------------------test6-----------------------
{
  "layer1": {
    "layer2": {
      "layer3_2": "string", 
      "layer3_1": [{"y": 7, "x": 1}, {"y": 4, "x": 0}, {"y": 3, "x": 5}, {"y": 9, "x": 6}]
    }
  }
}
Check: True
```
