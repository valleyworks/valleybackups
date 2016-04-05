from sys import platform as _platform

def get_platform():
  if _platform.startswith('linux'):
      return "linux"
  elif _platform == "darwin":
      return "osx"
  elif _platform == "win32":
     return "windows"
  else:
    return _platform
