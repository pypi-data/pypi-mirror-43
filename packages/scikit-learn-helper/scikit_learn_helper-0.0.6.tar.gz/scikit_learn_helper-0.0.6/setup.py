try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="scikit_learn_helper",
    version="0.0.6",
    author="Andres Arrieche",
    author_email="andres.arrieche.7@gmail.com",
    description="Helper code to make easier working with sklearn",
    packages=["."],
    download_url="https://pypi.org/project/scikit-learn-helper/#files",
    install_requires=["scikit-learn"],
    license="Apache",
    classifiers=["Programming Language :: Python", "License :: OSI Approved :: Apache Software License"]
)
