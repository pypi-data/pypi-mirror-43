try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="scikit_learn_helper",
    version="0.0.1",
    author="Andres Arrieche",
    author_email="andres.arrieche.7@gmail.com",
    description="Helper code to make easier working with sklearn",
    packages=["."],
    url="https://github.com/aras7/deployr-python-client",
    install_requires=["scikit-learn"],
    license="Apache",
    classifiers=["Programming Language :: Python", "License :: OSI Approved :: Apache Software License"]
)
