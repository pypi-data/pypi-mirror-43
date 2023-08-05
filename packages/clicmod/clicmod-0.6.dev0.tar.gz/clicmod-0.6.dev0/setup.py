from distutils.core import setup
import setuptools

setup(
    name='clicmod',
    version='0.6dev',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ['clicmod = impex.impex:main']
    },
    install_requires=[
        'requests',
        'urllib3',
        'pyfiglet'
    ],
    author="Nick Corso-Passaro",
    author_email="ncpassaro@gmail.com",
    description="A command line interface for IPsoft 1Desk content management.",
    long_description=open('README.md').read(),
)
