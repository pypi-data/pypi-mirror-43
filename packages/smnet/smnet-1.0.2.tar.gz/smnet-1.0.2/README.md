# SMNet
**A simple neural network framework.**

## Get start

### Installation

```
pip install smnet
```

## Try your first smnet program

```sh
$ python
```

```py
>>> import smnet as sm
>>> data_x = sm.Tensor(1)
>>> data_y = sm.Tensor([1, 2])
>>> data_flow = data_x + data_y
>>>
>>> sm.forward()
>>> print(data_flow.data)
[2. 3.]
```

Enter [examples dir](https://github.com/smarsuuuuuuu/SMNet/tree/master/examples) to learn more about smnet usage.
