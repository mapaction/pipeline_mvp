from typing import Optional


class FallbackDict:
    """
    TODO:
    Would be nice if this subclassed `dict` or something.

    The current implenmentation ensures that both the default and country specfic values 
    are available.
    """
    def __init__(self, default_values: Optional[dict], custom_values: Optional[dict]):
        self.default_values = default_values
        self.custom_values = custom_values

    def __getitem__(self, key):
        if self.custom_values is None or key not in self.custom_values:
            if isinstance(self.default_values[key], dict):
                return FallbackDict(self.default_values[key], None)
            else:
                return self.default_values[key]
        if isinstance(self.custom_values[key], dict):
            if self.default_values is not None and key in self.default_values:
                return FallbackDict(self.default_values[key], self.custom_values[key])
            else:
                return FallbackDict(None, self.custom_values[key])
        else:
            return self.custom_values[key]
