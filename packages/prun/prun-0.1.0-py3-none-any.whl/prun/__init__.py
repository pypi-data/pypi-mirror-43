import glob
import os
import sys
import subprocess


def main():
    # system dependent variables
    not_found_msg, exec_folder, exec_name = _get_system_specific_vars(sys.platform)

    # get the current working directory
    current_dir = os.getcwd()

    # get the command line arguments
    cli_args = sys.argv[1:]

    # search the python executable folder in the current working directory
    python_exec = search_python_in_folder_structure(current_dir, exec_folder, exec_name)
    if python_exec is None:
        raise ValueError('No virtual environment was found')
    python_folder = os.path.dirname(python_exec)

    # process the command line arguments for special tasks
    cli_args = process_cli_args(cli_args=cli_args)

    # Add the python executable folder to the path environment variable
    os.environ['PATH'] = os.pathsep.join([python_folder, os.environ.get('PATH', '')])

    # Run the command
    try:
        p = subprocess.Popen(cli_args, universal_newlines=True)
        p.communicate()
        sys.exit(p.returncode)
    except FileNotFoundError:
        print(not_found_msg % cli_args[0])
        sys.exit(1)


def _get_system_specific_vars(platform):
    if platform == 'win32':
        not_found_msg = "'%s' is not recognized as an internal or external command, " \
                        "operable program or batch file."
        exec_folder, exec_name = 'Scripts', 'python.exe'
    else:
        not_found_msg = '%s: command not found'
        exec_folder, exec_name = 'bin', 'python'
    return not_found_msg, exec_folder, exec_name


def process_cli_args(cli_args):
    """
    Process the list of command line arguments.

    Args:
        cli_args (list of str): list of command line arguments

    Returns:
        list of str: processed list of command line arguments
    """
    if len(cli_args) == 0:
        # if no cli args, add python
        cli_args = ['python']
    elif cli_args[0].endswith('.py'):
        # if first argument is a python file, add python
        cli_args = ['python'] + cli_args
    elif cli_args[0] == '-show':
        # if first argument is -show, show the path to the found python
        cli_args = ['which', 'python']
    elif cli_args[0] == '-h' or cli_args[0] == '-help':
        print('prun help: \n'
              '  Running a command using the local virtual environment:\n'
              '    prun command arg1 arg2 ...\n'
              '  Running python from the local virtual environment:\n'
              '    prun\n'
              '  Running a python file from the locql virtuql environment:\n'
              '    prun script.py arg1 arg2\n'
              '  Show the path to the python executable of the virtual environment:\n'
              '    prun -show\n'
              '  Show the prun help\n'
              '    prun -h')
        sys.exit(0)
    return cli_args


def search_python_in_folder_structure(folder, exec_folder_name, exec_name, max_search_depth=100):
    """
    Search a folder structure for a virtual environment python executable.

    Args:
        folder (str): the folder to start the search
        exec_folder_name (str): folder name of python executable
        exec_name (str): name of python executable
        max_search_depth (int): maximum upward search depth

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    folder_name = None
    for i in range(max_search_depth):
        if folder_name == '':
            break

        python_exec = find_virtual_environment(folder, exec_folder_name, exec_name)
        if python_exec is not None:
            return python_exec

        folder, folder_name = os.path.split(folder)
    return None


def find_virtual_environment(folder, exec_folder_name, exec_name):
    """
    Search a single folder for a virtual environment python executable.

    Args:
        folder (str): folder to find the virtual environment python executable in
        exec_folder_name (str): folder name of python executable
        exec_name (str): name of python executable

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    glob_paths = [os.path.join(folder, '*', exec_folder_name, exec_name),
                  os.path.join(folder, '.?*', exec_folder_name, exec_name)]

    python_exec = None
    for glob_path in glob_paths:
        try:
            python_exec = glob.glob(glob_path)[0]
        except IndexError:
            continue
        break

    return python_exec
