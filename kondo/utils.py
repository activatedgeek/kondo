from typing import NamedTuple


class Spec(NamedTuple):
  group: str
  params: dict
  n_trials: int = 0


class Nop:
  """A NOP class. Give it anything."""
  def nop(self, *args, **kwargs):
    pass

  def __getattr__(self, _):
    return self.nop
