#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Разработайте аналог утилиты tree в Linux. Используйте возможности модуля argparse для
# управления отображением дерева каталогов файловой системы. Добавьте дополнительные
# уникальные возможности в данный программный продукт.

import argparse
import os

def tree(directory, level=0, show_hidden=False, show_size=False):
    """
    Prints a tree representation of the specified directory.

    Args:
        directory (str): The directory to display.
        level (int): The current level of the tree.
        show_hidden (bool): Whether to show hidden files and directories.
        show_size (bool): Whether to show the size of each file.
    """

    # Get the list of files and directories in the specified directory.
    entries = os.listdir(directory)

    # If the show_hidden flag is False, filter out hidden files and directories.
    if not show_hidden:
        entries = [entry for entry in entries if not entry.startswith('.')]

    # Print the indentation for the current level.
    print(' ' * level * 4, end='')

    # Iterate over the list of files and directories.
    for entry in entries:
        # Get the full path to the entry.
        path = os.path.join(directory, entry)

        # If the entry is a directory, print its name and recurse into it.
        if os.path.isdir(path):
            print(f'{entry}/')
            tree(path, level + 1, show_hidden, show_size)

        # If the entry is a file, print its name and size (if the show_size flag is True).
        else:
            if show_size:
                size = os.path.getsize(path)
                print(f'{entry} ({size} bytes)')
            else:
                print(entry)


def main() -> object:
    # Create an ArgumentParser object.
    parser = argparse.ArgumentParser(description='Tree utility')

    # Add arguments to the parser.
    parser.add_argument('directory', nargs='?', default=os.getcwd(), help='The directory to display')
    parser.add_argument('-a', '--show-hidden', action='store_true', help='Show hidden files and directories')
    parser.add_argument('-s', '--show-size', action='store_true', help='Show the size of each file')
    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    # Parse the arguments.
    args = parser.parse_args()

    # Print the tree representation of the specified directory.
    tree(args.directory, show_hidden=args.show_hidden, show_size=args.show_size)


if __name__ == '__main__':
    main()
