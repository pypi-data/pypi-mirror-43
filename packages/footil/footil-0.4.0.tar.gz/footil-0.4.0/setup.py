from distutils.core import setup

setup(
    name='footil',
    version='0.4.0',
    packages=['footil'],
    license='LGPLv3',
    url='https://github.com/focusate/footil',
    description="Various Python helpers for other projects",
    long_description=open('README.rst').read(),
    install_requires=['yattag'],
    maintainer='Andrius Laukavičius',
    maintainer_email='dev@focusate.eu',
    python_requires='>=3',
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
