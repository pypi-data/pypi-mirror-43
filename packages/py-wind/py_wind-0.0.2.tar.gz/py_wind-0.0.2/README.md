# py_wind
wind 接口简易封装

## 环境需求
* python 3.6+

## 使用说明
    更多函数用法,详见函数说明.
    
### 示例
```python
from py_wind.wind import Wind, StockTick

def OnTick(tick:StockTick):
    print(tick.__dict__)

if __name__ == '__main__':
    s = Wind()
    # 历史行情
    df = s.get_history_min('000001.SZ', '2019-01-01', period=5)
    print(df)
    # 实时行情
    s.on_tick = OnTick
    s.sub_quote('000001.SZ')
    while input() != 'q':
        continue
    s.stop()

```

