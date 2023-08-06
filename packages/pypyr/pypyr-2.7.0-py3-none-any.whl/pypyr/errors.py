"""Custom exceptions for pypyr.

All pypyr specific exceptions derive from Error.
"""


class Error(Exception):
    """Base class for all pypyr exceptions."""


class ContextError(Error):
    """Error in the pypyr context."""


class KeyInContextHasNoValueError(ContextError):
    """pypyr context[key] doesn't have a value."""


class KeyNotInContextError(ContextError, KeyError):
    """Key not found in the pypyr context."""
    def __str__(self):
        """KeyError has custom error formatting, avoid this behaviour."""
        return super(Exception, self).__str__()


class LoopMaxExhaustedError(Error):
    """Max attempts reached during looping."""


class PipelineDefinitionError(Error):
    """Pipeline definition incorrect. Likely a yaml error."""


class PipelineNotFoundError(Error):
    """Pipeline not found in working dir or in pypyr install dir."""


class PlugInError(Error):
    """Pypyr plug-ins should sub-class this."""


class PyModuleNotFoundError(Error, ModuleNotFoundError):
    """Could not load python module because it wasn't found."""
