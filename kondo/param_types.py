import abc
import numpy as np


class ParamType(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def sample(self, size=1):
    raise NotImplementedError
  

class ChoiceType(ParamType):
  def __init__(self, values: list):
    self.values = values

  def sample(self, size=1):
    return np.random.choice(self.values, size=size)


class RandIntType(ParamType):
  def __init__(self, low=0, high=1):
    self.low = low
    self.high = high + 1

  def sample(self, size=1):
    return np.random.randint(self.low, self.high, size=size)


class UniformType(ParamType):
  def __init__(self, low=0.0, high=1.0):
    self.low = low
    self.high = high

  def sample(self, size=1):
    return np.random.uniform(self.low, self.high, size=size)


class LogUniformType(UniformType):
  def __init__(self, low=0.0, high=1.0):
    super().__init__(low=np.log(low), high=np.log(high))

  def sample(self, size=1):
    return np.exp(super().sample(size=size))


class NormalType(ParamType):
  def __init__(self, mu=0.0, sigma=1.0):
    self.mu = mu
    self.sigma = sigma

  def sample(self, size=1):
    return np.random.normal(self.mu, self.sigma, size=size)


class LogNormalType(ParamType):
  def __init__(self, mu=0.0, sigma=1.0):
    self.mu = mu
    self.sigma = sigma

  def sample(self, size=1):
    return np.random.lognormal(self.mu, self.sigma, size=size)
