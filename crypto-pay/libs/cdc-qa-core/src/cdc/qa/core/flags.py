"""Implementation of a layered flag object.

See `Flags` for implementation details.

Usage example:

    # Create Flags objects
    parent_flags = Flags("Parent Flags", {"FLAG_A": {"type": str, "default": "some value"}})
    child_flags = Flags("Child Flags", {"FLAG_B": {"type": str, "default": "other value"}}, parent_flags)

    # Child inherits flags from parent
    print(child_flags.FLAG_A)

    # Child can override parent
    child_flags.FLAG_A = "override parent's value"
    print(child_flags.FLAG_A)

    # Override can be deleted
    delattr(child_flags, "FLAG_A")
    print(child_flags.FLAG_A)
"""
from typing import Optional, Any, Type
import logging
import distutils.util

logger = logging.getLogger(__name__)


def type_cast(value: Any, target_type: Type[Any]):
    """Cast `value`'s type into `target_type`.

    Mostly exists since type casting bool requires special handling.

    Args:
        value (Any): Value to be type casted.
        target_type (Type[Any]): The type to be casted into.

    Returns:
        The type casted value.
    """
    if type(value) is not target_type:
        if target_type is bool:
            value = distutils.util.strtobool(value)
        value = target_type(value)
    return value


class Flags:
    """An object containing a defined set of flags.

    Defining flags:
        The set of available flags is defined on object initialization, and defaults will be added to the object as
        attributes. This set of flags will restrict how this `Flags` object can be interacted with.

    Getting flags:
        Flags can only be get if defined on initialization or inherited from parents. Flags that are inherited are not
        added to attributes unless set explicitly, and will get its value directly from its parent.

    Setting flags:
        Flags can only be set if defined on initialization or inherited from parents. If flags that are not defined but
        inherited is set explicitly, it is considered an 'override' and will be added to attributes of the object, and
        getting the value will no longer involves its parent. This 'override' can be removed by deleting the attribute.


    Properties:
        flags(dict): All flags available, including both defined and inherited.
        dict(dict): All values of available flags, including both defined and inherited.
    """

    def __init__(self, name: str, flags: dict, parent: Optional["Flags"] = None):
        """Inits Flags.

        Args:
            name (str): Name of this set of flags.
            flags (dict): dict mapping for defining flags.
                Each item should includes a sub-dict with keys "type" and "default".
            parent (Optional[, optional): Parent flags of this set of flags. Defaults to None.
        """
        self._name: str = name
        self._flags: dict = flags
        self._parent: Optional[Flags] = parent

        for key, value in self._flags.items():
            setattr(self, key, value["default"])

    @property
    def flags(self) -> dict:
        return {**self._parent.flags, **self._flags} if self._parent else self._flags

    @property
    def dict(self) -> dict:
        return {**self._parent.dict, **self.__dict__} if self._parent else self.__dict__

    def __str__(self):
        return f"<{self.__class__.__name__}: {self._name}>"

    def __getattr__(self, name):
        if name.startswith("_"):
            super(Flags, self).__getattribute__(name)
        else:
            if name not in self.flags:
                raise AttributeError(f"{self} Flag [{name}] is not a defined flag.")
            elif name not in self.__dict__ and self._parent:
                return getattr(self._parent, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super(Flags, self).__setattr__(name, value)
        else:
            try:
                if name not in self.flags:
                    raise AttributeError(f"{self} Flag [{name}] is not a defined flag.")
                else:
                    super(Flags, self).__setattr__(name, type_cast(value, self.flags[name]["type"]))

            except AttributeError as e:
                logger.error(e)
