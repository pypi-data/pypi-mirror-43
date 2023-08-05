from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="yapayzeka",
    version="0.0.15",
    author="oguzhan",
    author_email="oguzhan_687@hotmail.com",
    description="makine öğrenimi denemesi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oguz687/netinterface",
    license="MIT",
    packages=["yapayzekainterface"],
    package_dir={"yapayzekainterface": "yapayzekainterface/"},
    package_data={"yapayzekainterface": ["modeller/*.pkl"]},
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)