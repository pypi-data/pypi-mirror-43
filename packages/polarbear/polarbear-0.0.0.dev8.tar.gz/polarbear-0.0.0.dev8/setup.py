from setuptools import setup

setup(name='polarbear',
      version='0.0.0.dev8',
      description='logic for social science survey data',
      packages=['polarbear'],
      install_requires=[
            'pandas',
            'savReaderWriter',
            'sqlalchemy',
            'xlrd',
            'openpyxl'
        ]
      )
