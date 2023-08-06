from setuptools import setup

setup(
    name="rv-schubert-sdk",
    author="Raphael Schubert",
    author_email="rfswdp@gmail.com",
    description="SKD de integracao com RV Tecnologia",
    url="https://github.com/rfschubert/rv-schubert-sdk",
    version='0.0.1',
    packages=['rv_schubert_sdk'],
    install_requires=[
        'xmltodict',
        'json',
        'requests',
        'pendulum',
    ],
    include_package_data=True,
)
