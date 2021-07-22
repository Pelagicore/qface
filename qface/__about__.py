import os.path

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "qface"
__summary__ = "A generator framework based on a common modern IDL"
__url__ = "https://pelagicore.github.io/qface/"
__version__ = "2.0.5"
__author__ = "JRyannel"
__author_email__ = ""
__copyright__ = "2019 Pelagicore"
