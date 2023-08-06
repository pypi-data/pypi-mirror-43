import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bane",
    version="1.4.1",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    package_data={'bane':'bane'},
    description="cyber security library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/bane",
    packages=setuptools.find_packages(),
    python_requires=">=2.7",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: Unix",
    ],
)
