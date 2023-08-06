__version__ = '0.4.0'

try:
  from rainbow.rainbow import RainbowLogger
except ImportError:
  from rainbow import RainbowLogger
