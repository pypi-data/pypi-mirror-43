import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alfred-installer",
    version="0.1.2",
    author="David Vilela",
    author_email="dvilelaf@gmail.com",
    description="A script to install all your favourite applications and perform the most common tasks in Debian, Ubuntu and derivatives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derkomai/alfred",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": [
            "alfred-installer=alfred.__main__:main",
        ]
    }
)
