from setuptools import setup
import os

import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)
    
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

reqired_packages=[
    'PyQt5>=5.0',
    'numpy>=1.16',
    'matplotlib>=3.0',
    'sounddevice',
    'soundfile',
    'scipy>=1.2',
    ]

setup(name='acomod',
      version='0.1',
      description='Acoustic Oscillations Viewer',
      long_description=read('README.md'),
      author='Bartosz Lew',
      author_email='bartosz.lew@protonmail.com',
      url='https://github.com/bslew/acomod',
      install_requires=reqired_packages,
      package_dir = {'': 'src'},
      packages = ['acomod',
                  ],
      entry_points={ 'gui_scripts': [ 'acoustic_mode_viewer = acomod.sonidist:main',
               ],
                    },
      package_data={'acomod': ['*.ui',
                               ]},
      eager_resources={'acomod': ['data/*.wav','data/*.WAV',
                               ]},
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
        ],
     )
