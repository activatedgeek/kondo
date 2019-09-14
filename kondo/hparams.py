import os
import time
import inspect
from ruamel import yaml
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
             ignore_groups: Optional[List[str]] = None,
             trials_dir: Optional[str] = None) -> Generator[dict, None, None]:
    if trials_dir is not None:
      trials_dir = os.path.abspath(trials_dir)
      os.makedirs(trials_dir, exist_ok=True)

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

        trial = {**self._hparams, **t_rvs}

        if trials_dir is not None:
          name = '{}-{}-{}'.format(self.exp_class.__name__,
                                   spec.group,
                                   time.time())
          t_dir = os.path.join(trials_dir, name)

          os.makedirs(t_dir, exist_ok=True)
          with open(os.path.join(t_dir, 'trial.yaml'), 'w') as f:
            yaml.safe_dump({**trial, 'name': name, 'log_dir': t_dir},
                           stream=f, default_flow_style=False)

        yield trial
