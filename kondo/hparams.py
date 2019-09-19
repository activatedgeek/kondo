from time import strftime
from uuid import uuid4
import inspect
from typing import Generator, Optional, List

from .param_types import ParamType


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
             ignore_groups: Optional[List[str]] = None) \
             -> Generator[dict, None, None]:
    for spec in self.exp_class.spec_list():
      if groups is not None and spec.group not in groups:
        continue

      if ignore_groups is not None and spec.group in ignore_groups:
        continue

      rvs = {
          k: v.sample(size=spec.n_trials).tolist()
             if isinstance(v, ParamType) else v
          for k, v in spec.params.items()
      }

      for t in range(spec.n_trials):
        t_rvs = {k: v[t] if isinstance(v, list) else v
                 for k, v in rvs.items()}

        name = '{}-{}--{}--{}'.format(self.exp_class.__name__,
                                      spec.group,
                                      strftime('%m-%d-%Y-%H-%M-%S'),
                                      str(uuid4())[:8])

        trial = {**self._hparams, **t_rvs}

        yield name, trial

  @staticmethod
  def to_argv(trial: dict) -> List[str]:
    argv = []
    for k, v in trial.items():
      if v is not None:
        arg = '--{}'.format(k)

        if not isinstance(v, bool):
          arg = '{}={}'.format(arg, v)

        argv.append(arg)

    return argv
