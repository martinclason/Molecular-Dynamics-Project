
class ConfigError(Exception):
  """Used to raise errors when issues with the configuration file is encountered

  :param config_properties: properties involved in error
  :type config_properties: list of str
  :param message: message describing the error
  :type message: str
  """
  def __init__(self, config_properties, message):
    self.message = message
    self.config_properties = config_properties

  def __str__(self):
    return f"""{self.message}
Involved config properties: {", ".join(self.config_properties)}"""

