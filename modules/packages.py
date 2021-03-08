import random
import string
import struct
import itertools
import hashlib
import time
import multiprocessing as mp
import math

try:
    import os
except Exception:
    os = None

try:
    import numpy as np
except ModuleNotFoundError:
    np = None

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
except ModuleNotFoundError:
    Cipher = None
    algorithms = None
    modes = None


try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None
