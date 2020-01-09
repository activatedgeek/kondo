import itertools
from typing import Generator, List


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
