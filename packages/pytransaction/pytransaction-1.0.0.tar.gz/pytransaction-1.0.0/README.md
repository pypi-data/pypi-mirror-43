# 伪事务处理

## 功能

对于一组函数，如果执行过程中发生异常, 按照反向的调用顺序依次调用对应的逆过程


## 栗子

```python
from pytransaction import Transaction


def test1(*args, **kwargs):
    print('test1 running..', args, kwargs)


def test2(*args, **kwargs):
    print('test2 running...', args, kwargs)
    raise ValueError('oops, exception occurs')


def rollback(*args, **kwargs):
    print('rolling back...', args, kwargs)


try:
    with Transaction() as t:
        t.run(test1, rollback, args=(1,2), kwargs={'arg3':3}, rargs=('a', 'b'), rkwargs={'t':'tt'})
        t.run(test1, rollback, kwargs={'arg3':3})
        t.run(test1, rollback, args=(4,), kwargs={'a':'aa'}, rargs=(5,6), rkwargs='same')
        t.run(test2, rollback, args=('stop here',), rargs='same')
        t.run(test1, rollback, args=('will not run'))
except Exception as e:
    print('handle exceptions here')
    raise e

```


## 注意

因为逆向操作也可能会失败，因此不能完全保证事务一定得到处理