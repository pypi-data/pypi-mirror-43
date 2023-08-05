from pathlib import Path
from typing import Union


def write(file_path: Union[str, Path], content: Union[str, bytes], parents: bool = False) -> bool:
    """
    Write to file if content changed
    :param file_path: path in str or Path type
    :param content: string or bytes
    :param parents: make parent dir if True
    :return: write if True
    """
    binary = isinstance(content, bytes)

    if file_path.exists() and file_path.is_file():
        with open(str(file_path), 'rb' if binary else 'r') as f:
            if f.read() == content:
                return False

    if parents:
        Path(file_path.parent).mkdir(exist_ok=True, parents=True)
    with open(str(file_path), 'wb' if binary else 'w') as f:
        f.write(content)
    return True
