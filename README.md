# Kondo

[![Build Status](https://travis-ci.com/activatedgeek/kondo.svg?branch=master)](https://travis-ci.com/activatedgeek/kondo)
[![PyPI version](https://badge.fury.io/py/kondo.svg)](https://pypi.org/project/kondo/)
![Alpha](https://img.shields.io/badge/status-beta-orange.svg)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)


![Marie Kondo Spark Joy](https://i.imgflip.com/2zdobd.jpg)

The name is inspired by [Marie Kondo](https://konmari.com)'s tidying adventures.

Throw away experiments that don't spark joy with this tiny framework agnostic
module.

## Installation

### PyPI

```
pip install kondo
```

### Source

```
pip install git+https://github.com/activatedgeek/kondo.git@master
```

**NOTE**: Prefer pinning to a reference than the master branch for unintended updates.

## Usage

* Create new `Experiment` class
  ```python
  from kondo import Experiment, RandIntType, ChoiceType

  class MyExp(Experiment):
    def __init__(self, foo=100, bar='c', **kwargs):
      super().__init__(**kwargs)
      self.foo = foo
      self.bar = bar

    def run(self):
      print('Running experiment with foo={}, bar="{}".'.format(self.foo, self.bar))

    @staticmethod
    def spec_list():
      return [
        ('example', 3, dict(
          foo=RandIntType(low=10, high=100),
          bar=ChoiceType(['a', 'b', 'c']),
        ))
      ]
  ```
  Make sure to capture all keyword arguments to the super class using `**kwargs`
  as above.

* Create `Hyperparameter` spec
  ```python
  from kondo import HParams
  
  hparams = HParams(MyExp)
  ```
  `HParams` class automagically recognizes all the possible parameters to the
  experiment specified as arguments to the constructor with default values. The
  `spec` can be any key value pairs (and can include constant values which will
  remain common across all trials).

  Other types available can be seen in [param_types.py](./kondo/param_types.py).

* Generate trials and create a new experiment each time
  ```python
  for trial, _ in hparams.trials():
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

* We can alternatively save this configurations for later use and load the experiment
  on demand. We extend the above example by making the following calls
  ```python
  import os

  trials_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.trials')
  hparams.save_trials(trials_dir)
  ```

  We then load all of the saved trials from the `YAML` files.
  ```python
  import glob

  for fname in glob.glob('{}/**/trial.yaml'.format(trials_dir)):
    trial, _ = MyExp.load(fname, run=False)

    exp = MyExp(**trial)
    exp.run()
  ```

Now, you can keep tuning the spec during your hyperparameter search and *throw
away the ones that don't spark joy*!.

The full example file is available at [basic.py](./examples/basic.py).

## License

Apache 2.0