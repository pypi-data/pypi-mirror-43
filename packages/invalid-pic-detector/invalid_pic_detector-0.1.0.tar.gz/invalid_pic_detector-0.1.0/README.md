# IPD

图片有效性检测（是否为黑/白屏）

## 使用

```python
import ipd


result = ipd.detect('1.png', 255)
print('white: ', result)
```

output:

```shell
2019-03-05 15:09:09.651 | DEBUG    | ipd:detect:38 - analysing picture: [1.png]
2019-03-05 15:09:09.656 | DEBUG    | ipd:_load_from_path:22 - <IPDPicture 749x819 from F:\IPD\1.png> loaded
white:  0.45025101770307674
```

## 参考数据

- 正常情况：
    - black：< 0.01
    - white：< 0.95
- 纯白屏
    - white：> 0.99
- 纯黑屏
    - black：> 0.50
