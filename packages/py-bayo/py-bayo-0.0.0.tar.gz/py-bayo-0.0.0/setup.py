from setuptools import setup
from pathlib import Path
import random
import string

Path(
    '/tmp/py-pypi-org-bayo-deleted-%s' % 
    ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
).touch()

setup(
    name = 'py-bayo',
    version = '0.0.0',
    description = 'This is a dummy package.',
)
