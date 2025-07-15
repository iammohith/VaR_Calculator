from setuptools import setup, find_packages

setup(
    name='VaR_Calculator',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',
        'numpy',
        'pandas',
        'scipy',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'var-calculator=var_calculator.cli:main',
        ],
    },
)
