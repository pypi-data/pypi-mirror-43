from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="rv-schubert-sdk",
    author="Raphael Schubert",
    author_email="rfswdp@gmail.com",
    description="SKD de integracao com RV Tecnologia",
    url="https://github.com/rfschubert/rv-schubert-sdk",
    version='0.0.2',
    packages=['rv_schubert_sdk'],
    long_description=readme,
    license=license,
    install_requires=[
        'xmltodict',
        'json',
        'requests',
        'pendulum',
    ],
    include_package_data=True,
)
