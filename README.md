# Kondo

> Does your experiment spark joy?

Throw away experiments that don't spark joy with this tiny framework agnostic
module.

## Installation

### PyPI

TODO.

### Source

```
pip install git+https://github.com/activatedgeek/kondo.git@master
```

## Usage

* Create new `Experiment` class
  ```python
  from kondo import Experiment

  class MyExp(Experiment):
    def __init__(self, foo=100, bar='c', **kwargs):
      super(MyExp, self).__init__(**kwargs)
      self.foo = foo
      self.bar = bar

    def run(self):
      print('Running experiment with foo={}, bar={}!'.format(self.foo, self.bar))
  ```
  Make sure to capture all keyword arguments to the super class using `**kwargs`
  as above.

* Create `Hyperparameter` spec
  ```python
  from kondo import HParams, RandIntType, ChoiceType

  spec = dict(
    foo=RandIntType(low=10, high=100),
    bar=ChoiceType(['a', 'b', 'c']),
  )
  
  hparams = HParams(MyExp, spec)
  ```
  `HParams` class automagically recognizes all the possible parameters to the
  experiment specified as arguments to the constructor with default values. The
  `spec` can be any key value pairs (and can include constant values which will
  remain common across all trials).

  Other types available can be seen in [param_types.py](./kondo/param_types.py).

* Generate trials and create a new experiment each time
  ```python
  for trial in hparams.trials(num=3):
    exp = MyExp(**trial)
    exp.run()
  ```

  A sample output for these three trials with randomly selected values for `foo`
  and `bar` is shown below. Each line represents the dictionary sent in to the
  constructor of the `MyExp` class.

  ```shell
  Running experiment with foo=93, bar="b".
  Running experiment with foo=30, bar="c".
  Running experiment with foo=75, bar="c".
  ```

  Now, you can keep tuning the spec during your hyperparameter search and *throw
  away the ones that don't spark joy!*.

  The full example file is available at [basic.py](./examples/basic.py).

## License

Apache 2.0