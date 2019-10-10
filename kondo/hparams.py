import math
from time import strftime
from uuid import uuid4
import inspect
from typing import Generator, Optional, List, Tuple, Callable

from .param_types import ParamType
from .utils import Spec


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

  def resolve_spec(self, spec: Spec) -> Generator[Tuple[str, dict], None, None]:
    rvs = {
        k: v.sample(size=spec.n_trials).tolist()
           if isinstance(v, ParamType) else v
        for k, v in spec.params.items()
    }

    uuid_str = str(uuid4())[:8]
    time_str = strftime('%Y_%m_%d-%H_%M_%S')
    n_pad = int(math.log10(spec.n_trials)) + 1

    for t in range(spec.n_trials):
      t_rvs = {k: v[t] if isinstance(v, list) else v
               for k, v in rvs.items()}

      name = '{cls_name}-{group}-{time_str}-{t:0{n_pad}d}-{uuid_str}'.format(
          t=t + 1, n_pad=n_pad, cls_name=self.exp_class.__name__,
          group=spec.group, time_str=time_str, uuid_str=uuid_str)

      trial = {**self._hparams, **t_rvs}

      yield name, trial

  def trials(self,
             groups: Optional[List[str]] = None,
             ignore_groups: Optional[List[str]] = None,
             spec_func: Optional[Callable[[], List[Spec]]] = None) \
             -> Generator[Tuple[str, dict], None, None]:

    spec_func = spec_func or self.exp_class.spec_list
    for spec in spec_func():
      if groups is not None and spec.group not in groups:
        continue

      if ignore_groups is not None and spec.group in ignore_groups:
        continue

      yield from self.resolve_spec(spec)

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
