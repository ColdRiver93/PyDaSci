from setuptools import setup

__version__ = '1.0.0'


def readme():
    with open('readme.txt') as f:
        return f.read()


setup(
    name='pydasci',
    version=__version__,
    description="Python Data Science Domain Specific Language.",
    long_description=readme(),
    author='Juan Riofrio',
    author_email='jriofrio93@gmail.com',
    keywords='timeseries forecasting datascience',
    entry_points={
        'console_scripts': ['pydasci = pydasci.main_pds:main']
    },
    license='Yacahy Tech',
    packages=['pydasci'],
    install_requires=['rply','matplotlib','statsmodels','numpy', 'Cython', 'scipy','scikit-learn'],
    classifiers=['Intended Audience :: Classmates'],
    zip_safe=False,
)