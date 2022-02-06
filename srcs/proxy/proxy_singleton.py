"""

[proxy] proxy_singleton.py

Author: seith <seith.corp@gmail.com>

Created: 06/02/2021 22:32:00 by seith
Updated: 06/02/2021 22:32:00 by seith

Synezia Corp. (c) 2021 - MIT

"""


class ProxySingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
