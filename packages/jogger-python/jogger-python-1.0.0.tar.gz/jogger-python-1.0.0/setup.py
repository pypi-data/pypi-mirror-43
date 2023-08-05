from setuptools import setup, find_packages

with open('./version.txt', 'r') as v:
    version = v.read()

setup(
    name='jogger-python',
    version=version,
    description='Johnny Logger (Jogger) in Python3',
    url='http://github.com/theonlyjohnny/jogger-python',
    author='Johnny Dallas',
    author_email='theonlyjohnny@theonlyjohnny.sh',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'colorlog'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False
)
