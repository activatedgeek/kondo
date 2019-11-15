import os
import random
from typing import Optional, List, Tuple, Any, Union
import logging
import numpy as np

from .hparams import Spec
from .utils import Nop


class Experiment:
  def __init__(self,
               seed: Optional[int] = None,
               log_dir: Optional[str] = None,
               log_int: int = 100,
               ckpt_int: int = 100):

    self._seed = self._set_seeds(seed)

    self._cuda = self._find_cuda()

    self._log_dir, self._logger = self._prep_logger(log_dir)
    self._log_int = log_int
    self._ckpt_int = ckpt_int

    self._params_accum = dict(seed=self._seed)

  @staticmethod
  def spec_list() -> List[Spec]:
    '''
    A list of named-tuples containing name
    of the spec, number of trials to generate
    and an arbitrary parameter dictionary. See examples.
    '''
    raise NotImplementedError

  def run(self):
    raise NotImplementedError

  @property
  def seed(self) -> Optional[int]:
    return self._seed

  @property
  def cuda(self) -> bool:
    return self._cuda

  @property
  def log_dir(self) -> Optional[str]:
    return self._log_dir

  @property
  def log_interval(self) -> int:
    return self._log_int

  @property
  def ckpt_interval(self) -> int:
    return self._ckpt_int

  @property
  def logger(self) -> Union[Any, Nop]:
    return self._logger or Nop()

  @property
  def params_acc(self) -> dict:
    assert isinstance(self._params_accum, dict), \
      'did you forget to call super()?'

    return self._params_accum

  @params_acc.setter
  def params_acc(self, newparams: dict):
    assert isinstance(self._params_accum, dict), \
      'did you forget to call super()?'

    self._params_accum.update(newparams)

  def _set_seeds(self, seed: Optional[int]) -> Optional[int]:
    if seed:
      random.seed(seed)
      np.random.seed(seed)

      try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
      except ModuleNotFoundError:
        logging.warning('torch not seeded because import failed.')

    return seed

  def _find_cuda(self) -> bool:
    try:
      import torch
      return torch.cuda.is_available()
    except ModuleNotFoundError:
      logging.warning('"cuda" set to `False` because "import torch" failed.')
      return False

  def _prep_logger(self, log_dir) -> Tuple[Optional[str], Optional[Any]]:
    logger = None
    if log_dir:
      try:
        from torch.utils.tensorboard import SummaryWriter
        log_dir = os.path.abspath(log_dir)
        logger = SummaryWriter(log_dir)
      except ModuleNotFoundError:
        logging.warning('"log_dir" and logger" set to `None` because "SummaryWriter" could not be imported.') # pylint: disable=line-too-long
        log_dir = None

    return log_dir, logger
