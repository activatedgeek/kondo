import itertools
import inspect
from typing import Generator, List, Dict



def read_params_from_class(cls_object, ax_params=False) -> List[Dict]:
  '''Read all default arguments from a class constructor.

  NOTE: also follows parents.
  '''
  attribs = {}

  for sup_c in type.mro(cls_object)[::-1]:
    argspec = inspect.getfullargspec(getattr(sup_c, '__init__'))
    argsdict = dict(dict(zip(argspec.args[1:], argspec.defaults or [])))
    attribs = {**attribs, **argsdict}

  # Ignore all keys with null values.
  attribs = {k: v for k, v in attribs.items() if v is not None}

  # generate a list of fixed parameters in
  # Adaptive Experimentation framework format.
  if ax_params:
    attribs = [
        dict(name=k, type='fixed', value=v)
        for k, v in attribs.items()
    ]

  return attribs


def exhaust_params(params: dict) \
  -> Generator[dict, None, None]:
  '''Compute cross-product of all lists.
  '''
  if len(params) == 0:
    return []

  params = {k: v if isinstance(v, list) else [v] for k, v in params.items()}
  keys, values = zip(*params.items())

  for p in itertools.product(*values):
    yield dict(zip(keys, p))


def to_argv(trial: dict) -> List[str]:
  '''Convert key-value dictionary into CLI argument list.
  '''
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


class Nop:
  """A NOP class. Give it anything."""
  def nop(self, *args, **kwargs):
    pass

  def __getattr__(self, _):
    return self.nop
