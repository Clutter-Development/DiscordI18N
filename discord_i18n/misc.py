from typing import TypeVar

__all__ = ("find_in_nested_dict", "NestedDict")

T = TypeVar("T")
T2 = TypeVar("T2")
NestedDict = dict[str, T | "Nest[T]"]


def find_in_nested_dict(
    find_in: NestedDict[T], path: str | list[str], /, *, default: T2 = None
) -> T | T2:
    """Finds the value that is in the path.
    Args:
        find_in (NestedDict): The dictionary to get the value from.
        path (str | list[str]): The path to the value.
        default (Any, optional): The default value to return if the key is not found. Defaults to None.
    Returns:
        Any: The value. Returns the default value if the key is not found.
    """
    if isinstance(path, str):
        return find_in_nested_dict(find_in, path.split("."), default=default)

    for key in path:
        try:
            find_in = find_in[key]
        except (KeyError, TypeError):
            return default

    return find_in
