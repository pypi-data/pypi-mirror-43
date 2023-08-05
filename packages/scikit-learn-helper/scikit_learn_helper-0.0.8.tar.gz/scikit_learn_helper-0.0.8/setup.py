from setuptools import find_packages, setup

setup(
    name="scikit_learn_helper",
    version="0.0.8",
    author="Andres Arrieche",
    author_email="andres.arrieche.7@gmail.com",
    description="Helper code to make easier working with sklearn",
    packages=find_packages(),
    include_package_data=True,
    download_url="https://pypi.org/project/scikit-learn-helper/#files",
    install_requires=["scikit-learn"],
    license="Apache",
    classifiers=["Programming Language :: Python", "License :: OSI Approved :: Apache Software License"]
)
