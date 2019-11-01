import math
import itertools
from collections import defaultdict
from time import strftime
from uuid import uuid4
import inspect
from typing import Generator, Optional, List, Tuple, Callable

from .param_types import ParamType


class Spec:
  def __init__(self,
               group: str = '',
               exhaustive: bool = False,
               params: dict = None,
               n_trials: int = 0):
    self.group = group
    self.exhaustive = exhaustive
    self.params = params
    self.n_trials = n_trials

    if self.exhaustive:
      self.n_trials, self.params = self._exhaust_params(params)

  @staticmethod
  def _exhaust_params(params: dict) -> dict:
    for k, v in params.items():
      assert not isinstance(v, ParamType), \
        '"{}" not supported in exhaustive mode'.format(v.__class__.__name__)

    scalar_params = {k: v for k, v in params.items() if not isinstance(v, list)}
    list_params = defaultdict(list)
    list_keys, list_values = zip(*[(k, v) for k, v in params.items()
                                   if isinstance(v, list)])
    n_trials = 0
    for list_val in itertools.product(*list_values):
      for k, v in zip(list_keys, list_val):
        list_params[k].append(v)
      n_trials += 1

    return n_trials, {**scalar_params, **list_params}

  @staticmethod
  def get_unique_suffix():
    uuid_str = str(uuid4())[:8]
    time_str = strftime('%b%d-%H%M%S')
    return '{}-{}'.format(uuid_str, time_str)

  def resolve(self, base_hparams: Optional[dict] = None,
              name_prefix: str = '') \
    -> Generator[Tuple[str, dict], None, None]:
    rvs = {
        k: v.sample(size=self.n_trials).tolist()
           if isinstance(v, ParamType) else v
        for k, v in self.params.items()
    }

    suffix = self.get_unique_suffix()
    n_pad = int(math.log10(self.n_trials)) + 1

    for t in range(self.n_trials):
      t_rvs = {k: v[t] if isinstance(v, list) else v
               for k, v in rvs.items()}

      name = '{prefix}{group}-{t:0{n_pad}d}-{suffix}'.format(
          t=t + 1, n_pad=n_pad, group=self.group,
          prefix=name_prefix, suffix=suffix)

      trial = {**(base_hparams or {}), **t_rvs}

      yield name, trial


class HParams:
  def __init__(self, exp_class):
    self.exp_class = exp_class
    self._hparams = self.prep(exp_class)

  @property
  def hparams(self) -> dict:
    return self._hparams

  @staticmethod
  def prep(exp_class) -> dict:
    attribs = {}

    for sup_c in type.mro(exp_class)[::-1]:
      argspec = inspect.getfullargspec(getattr(sup_c, '__init__'))
      argsdict = dict(dict(zip(argspec.args[1:], argspec.defaults or [])))
      attribs = {**attribs, **argsdict}

    return attribs

  def trials(self,
             groups: Optional[List[str]] = None,
             ignore_groups: Optional[List[str]] = None,
             spec_func: Optional[Callable[[], List[Spec]]] = None) \
             -> Generator[Tuple[str, dict], None, None]:

    name_prefix = '{}-'.format(self.exp_class.__name__)
    spec_func = spec_func or self.exp_class.spec_list
    for spec in spec_func():
      if groups is not None and spec.group not in groups:
        continue

      if ignore_groups is not None and spec.group in ignore_groups:
        continue

      yield from spec.resolve(base_hparams=self._hparams,
                              name_prefix=name_prefix)

  @staticmethod
  def to_argv(trial: dict) -> List[str]:
    argv = []
    for k, v in trial.items():
      if v is not None:
        arg = ''
        if isinstance(v, bool):
          if v is True:
            arg = '--{}'.format(k)
        else:
          arg = '--{}={}'.format(k, v)

        if arg:
          argv.append(arg)

    return argv
