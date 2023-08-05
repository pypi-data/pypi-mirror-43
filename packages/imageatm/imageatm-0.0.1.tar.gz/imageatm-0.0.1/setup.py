from setuptools import setup, find_packages

setup(
    name='imageatm',
    version='0.0.1',
    author='Christopher Lennan, Malgorzata Adamczyk, Gunar Maiwald, Dat Tran',
    author_email='christopher.lennan@idealo.de, malgorzata.adamczyk@idealo.de, gunar.maiwald@idealo.de, dat.tran@idealo.de',
    description='Image classification for everyone',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    install_requires=['Keras>=2.2.4',
                      'keras-vis>=0.4.1',
                      'tensorflow>=1.12.0',
                      'awscli',
                      'Click',
                      'h5py',
                      'matplotlib',
                      'Pillow',
                      'python-dateutil',
                      'scikit-learn',
                      'scipy',
                      'tqdm',
                    ],
    extras_require={
        'tests': ['pytest',
                 'pytest-cov',
                 'pytest-mock',
                 'mock',
                 ]
    },
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    entry_points={'console_scripts': ['image-atm=imageatm.client.client:cli']},
)