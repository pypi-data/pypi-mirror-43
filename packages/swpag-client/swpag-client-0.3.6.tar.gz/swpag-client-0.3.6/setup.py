from distutils.core import setup

setup(
    name='swpag-client',
    version='0.3.6',
    description='This is a python module that provides an interface to the TeamInterface API.',
    packages=['swpag-client'],
    install_requires=[
        'requests',
        'future',
        'pyOpenSSL>=17.5.0',
        'urllib3>=1.22',
        'six>=1.11.0',
    ],
)
