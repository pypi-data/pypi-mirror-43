from .search import SearchAPI

__version__ = "1.0.3"
__author__ = "Ed Kohlwey"
__all__ = ["SearchAPI"]

if __name__ == "__main__":
    print("This module cannot be run on its own. Please use by running ",
          "\"from yanytapi import SearchAPI\"")
    exit(0)
