"""
:Author: Almer Mendoza
:Since: 10/10/2018
"""
_logging_module = None
_is_no_color = False

def _get_color(color=None):
  """Get color name from pre-defined color list"""
  if _is_no_color:
    return ''

  if color is None and not color:
    raise ValueError('Must have color code')

  colors = {
    'PURPLE':'\033[96m',
    'MAGENTA':'\033[95m',
    'BLUE':'\033[94m',
    'GREEN':'\033[92m',
    'YELLOW':'\033[93m',
    'RED':'\033[91m',
    'DARKGRAY':'\033[90m',
    'GREY':'\033[0m',
    'WHITE':'\033[1m'
  }

  if color not in colors:
    raise KeyError('Use a proper color name: {}'.format(list(colors.keys())))

  return colors[color]

def _get_message(no_time=False):
  """Get message parts"""
  time = '{}%(asctime)s{}'.format(_get_color('DARKGRAY'), _get_color('GREY'))
  name = '{}%(name)-12s{}'.format(_get_color('PURPLE'), _get_color('GREY'))
  level = '%(levelname)-8s'
  message = '%(message)s'

  if no_time:
    return '{} {}\t{}'.format(name, level, message)  

  return '{} {} {}\t{}'.format(time, name, level, message)

def _set_level_format(level=None, color='WHITE'):
  """Set logging format based on level and color"""
  FORMAT = '{}{}{}'
  parsed_format = FORMAT.format(
    _get_color(color),
    _logging_module.getLevelName(level),
    _get_color('GREY')
  )

  if level is not None:
    _logging_module.addLevelName(level, parsed_format)

  return True

def RainbowLogger(name=None, no_time=False, no_color=False, new_logging=None, filepath=None, log_level=None, get_logging=False):
  """A customized logger built on top of Python's logging"""
  import logging  
  global _logging_module
  global _is_no_color

  _is_no_color = no_color
  _logging_module = logging
  if new_logging is not None:
    _logging_module = new_logging

  _set_level_format(_logging_module.DEBUG, 'BLUE')
  _set_level_format(_logging_module.INFO, 'GREEN')
  _set_level_format(_logging_module.WARN, 'YELLOW')
  _set_level_format(_logging_module.ERROR, 'RED')
  _set_level_format(_logging_module.CRITICAL, 'MAGENTA')

  if name is None:
    logger = _logging_module
  else:
    logger = _logging_module.getLogger(name)

  handler = _logging_module.StreamHandler()
  final_message = _get_message(no_time)
  formatter = _logging_module.Formatter(final_message)

  handler.setFormatter(formatter)
  if name is None:
    _logging_module.basicConfig(format=final_message,
                                level=log_level if log_level else _logging_module.DEBUG)
  else:
    logger.addHandler(handler)
    logger.setLevel(log_level if log_level else _logging_module.DEBUG)

  if filepath and name:
    handler = _logging_module.FileHandler(filepath)
    _is_no_color = True
    final_message = _get_message(no_time)
    formatter = _logging_module.Formatter(final_message)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

  if get_logging:
    return _logging_module

  return logger

def __init__():
  return RainbowLogger
