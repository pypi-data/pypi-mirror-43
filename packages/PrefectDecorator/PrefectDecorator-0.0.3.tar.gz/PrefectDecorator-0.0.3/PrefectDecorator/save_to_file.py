"""A decorator that save the data to file."""

import os
import csv
from functools import wraps
from collections.abc import Iterable


def save_to_file(filepath, save=True, override=False, filetype='text', encoding='utf-8', end='\n', headers=None, process_func=None):
    """A decorator that save the data to file.
    
    Note:
        The arguments of the wrapped function can dynamically affect the function of the decorator.
        The arguments of the wrapped function have a higher priority.

    Args:
        filepath: The absolute path of the target file where the data is saved.
        save: A flag to save data.
        override: A flag to overwrite data in the target file.
        filetype: Type of target file.
        encoding: The encoding type of the data.
        end: The separator between each item if the data is iterable and the target file type is text.
        headers: This argument is valid only when saved as a csv file.
        process_func: The handler used in the iteration.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Must use 'nonlocal' keyword, otherwise the following error will be thrown.
            # UnboundLocalError: local variable 'xxx' referenced before assignment
            # Because of the internal implementation of Python, 
            # the assignment statement in the 'try' block makes 'xxx' be considered a local variable.
            # Arugment: headers also have same problem.
            nonlocal save, override, headers
            try:
                save = kwargs.pop('save')
            except KeyError:
                pass
            try:
                override = kwargs.pop('override')
            except KeyError:
                pass

            result = func(*args, **kwargs)  # Running internal function.
            
            if save:
                exist_flag = os.path.isfile(filepath)
                if exist_flag and not override:  # The data in the files is not overwirtten and the file exists.
                    return result
                elif exist_flag:  # Overwrite the data in the file and the file exists.
                    os.remove(filepath)  # Delete existing file.

                # Save to file.
                if filetype == 'text':
                    if isinstance(result, str):
                        with open(filepath, 'wt', encoding=encoding) as f:
                            if process_func is not None:
                                result = process_func(result)
                            f.write(str(result))
                    elif isinstance(result, list) or isinstance(result, tuple):
                        with open(filepath, 'at', encoding=encoding) as f:
                            for word in result:
                                if process_func is not None:
                                    word = process_func(word)
                                f.write(str(word) + end)
                    else:
                        raise TypeError('Data type are not supported: {}.'.format(type(result)))
                elif filetype == 'csv':
                    if isinstance(result, list) or isinstance(result, tuple):
                        with open(filepath, 'wt', encoding=encoding, newline='') as f:  # Avoid extra blank lines
                            f_csv = csv.writer(f)
                            if headers is None:
                                headers = ['-'] * len(result[0])  # Number of data items in the first line.
                                pass
                            f_csv.writerow(headers)
                            f_csv.writerows(result)
                else:  # Other types are not considered.
                    raise TypeError('Data type are not supported: {}.'.format(type(result)))
            else:
                pass

            return result
        return wrapper
    return decorate
