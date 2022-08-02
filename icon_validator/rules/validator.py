class KomandPluginValidator:
    """
    Class which can validate a Komand plugin or workflow.
    """

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    def validate(self, plugin_spec):
        pass
