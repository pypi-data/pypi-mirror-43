import glob
import os
import sys
import subprocess


def main():
    # get the current working directory
    current_dir = os.getcwd()

    # get the command line arguments
    cli_args = sys.argv[1:]

    # search the python executable folder in the current working directory
    python_exec = _search_python_in_folder_structure(current_dir)
    if python_exec is None:
        raise ValueError('No virtual environment was found')
    python_folder = os.path.dirname(python_exec)

    # if prun is called without arguments, python will be started
    if len(cli_args) == 0:
        cli_args = ['python']

    # Add the python executable folder to the path environment variable
    os.environ['PATH'] = os.pathsep.join([python_folder, os.environ.get('PATH', '')])

    # Run the command
    try:
        p = subprocess.Popen(cli_args, universal_newlines=True)
        p.communicate()
        sys.exit(p.returncode)
    except FileNotFoundError:
        if sys.platform == 'win32':
            print("'%s' is not recognized as an internal or external command, "
                  "operable program or batch file." % cli_args[0])
        else:
            print('%s: command not found' % cli_args[0])
        sys.exit(1)


def _search_python_in_folder_structure(folder, max_search_depth=100):
    """
    Search a folder structure for a virtual environment python executable.

    Args:
        folder (str): the folder to start the search
        max_search_depth (int): maximum upward search depth

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    folder_name = None
    for i in range(max_search_depth):
        if folder_name == '':
            break

        python_exec = _find_virtual_environment(folder)
        if python_exec is not None:
            return python_exec

        folder, folder_name = os.path.split(folder)
    return None


def _find_virtual_environment(folder):
    """
    Search a single folder for a virtual environment python executable.

    Args:
        folder (str): folder to find the virtual environment python executable in

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    glob_paths = _get_python_glob_paths(folder)

    python_exec = None
    for glob_path in glob_paths:
        try:
            python_exec = glob.glob(glob_path)[0]
        except IndexError:
            continue
        break

    return python_exec


def _get_python_glob_paths(folder):
    """
    Construct glob paths to find the virtual environment python executable based on the host system.

    Args:
        folder (str): base folder for the glob paths

    Returns:
        list of str: list of glob paths
    """
    if sys.platform == 'win32':
        # on windows python lives in <venv>/Scripts/python.exe
        glob_paths = [os.path.join(folder, '*', 'Scripts', 'python.exe'),
                      os.path.join(folder, '.?*', 'Scripts', 'python.exe')]
    else:
        # on osx and linux python lives in <venv>/bin/python
        glob_paths = [os.path.join(folder, '*', 'bin', 'python'),
                      os.path.join(folder, '.?*', 'bin', 'python')]
    return glob_paths
