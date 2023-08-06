from setuptools import setup

from pysqlitequeue import __version__


def setup_package():
    setup(name='PySqliteQueue',
          version=__version__,
          description='Sqlite based queue',
          author='Mark Andreev',
          author_email='mark.andreev@gmail.com',
          license='MIT License',
          platforms='any',
          packages=['pysqlitequeue'],
          classifiers=[
              'License :: OSI Approved :: MIT License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3.6',
              'Topic :: Software Development :: Libraries :: Python Modules',
          ]
          )


if __name__ == "__main__":
    setup_package()
