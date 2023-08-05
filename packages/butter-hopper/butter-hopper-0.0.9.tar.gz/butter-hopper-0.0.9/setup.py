from io import open

from setuptools import find_packages, setup

with open('butter_hopper/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

readme_file = 'README.md'

try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except ImportError:
    print ("m2r not found. Fallingback to direct markdown")
    with open(readme_file) as f:
        readme = f.read()

REQUIRES = ['click', 'shell', 'munch']

setup(
    name='butter-hopper',
    version=version,
    description='',
    long_description=readme,
    author='Cswl Coldwind',
    author_email='cswl1337@gmail.com',
    maintainer='Cswl Coldwind',
    maintainer_email='cswl1337@gmail.com',
    url='https://github.com/cswl/butter-hopper',
    license='MIT',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),

   entry_points = {
        'console_scripts': ['btrhop=butter_hopper.main:cli', 'bootcrap=butter_hopper.bootcrapper.main:cli'],
    },
)
