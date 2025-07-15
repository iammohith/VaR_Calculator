from setuptools import setup, find_packages

setup(
    name='var_calculator',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'var-calculator=cli:main',
        ],
    },
)
