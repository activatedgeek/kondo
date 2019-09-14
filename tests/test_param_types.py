import pytest
import numpy as np
from kondo.param_types import ParamType
from kondo import ChoiceType, RandIntType, UniformType, LogUniformType, NormalType, LogNormalType

@pytest.mark.parametrize('cls, kwargs', [
    (ChoiceType, dict(values=['a', 'b', 'c'])),
    (RandIntType, dict(low=80, high=90)),
    (UniformType, dict(low=0.0, high=1.0)),
    (LogUniformType, dict(low=0.0, high=1.0)),
    (NormalType, dict()),
    (LogNormalType, dict())
])
def test_basic_param_type(cls: ParamType, kwargs: dict):
  p = cls(**kwargs)
  rvs = p.sample()

  assert isinstance(rvs, np.ndarray)
  assert rvs.ndim == 1
