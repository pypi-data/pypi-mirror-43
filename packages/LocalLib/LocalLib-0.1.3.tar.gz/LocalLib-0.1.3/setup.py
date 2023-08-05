import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LocalLib",
    version="0.1.3",
    author="sudopigeek",
    author_email="samuelcatferrell@gmail.com",
    description="Makes easy tasks easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'': ['kjvdat.txt']},
    include_package_data=True,
    install_requires=[
        'win10toast>=0.9'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
