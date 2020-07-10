from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='cov19',
    version='0.0.8',
    url='https://github.com/emdemor/cov19',
    license='MIT License',
    author='Eduardo M. de Morais',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='emdemor415@gmail.com',
    keywords='covid-19',
    description=u'Prediction for the spread of COVID-19 using Epidemiological Models',
    packages=['cov19'],
    install_requires=['numpy','scipy','pandas','pygtc','setuptools','tqdm'],)