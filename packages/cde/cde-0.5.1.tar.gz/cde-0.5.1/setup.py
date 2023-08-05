from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='cde',
      version='0.5.1',
      long_description=long_description,
      description='Framework for conditional density estimation',
      url='https://jonasrothfuss.github.io/Nonparametric_Density_Estimation',
      author='Jonas Rothfuss, Fabio Ferreira',
      author_email='jonas.rothfuss@gmx.de, fabioferreira@mailbox.org',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'Keras',
        'numpy',
        'pandas',
        'tensorflow>=1.4,<=1.7.0',
        'matplotlib',
        'edward>=1.3.4,<=1.3.5',
        'seaborn',
        'scipy',
        'pytest',
        'scikit_learn',
        'statsmodels',
        'ml_logger<=99.99',
        'progressbar2'
      ],
      dependency_links=["https://github.com/jonasrothfuss/ml_logger/archive/9db50b24af8c5b29f229346325825328711f1aed.zip#egg=ml_logger-99.99"],
      zip_safe=False)
