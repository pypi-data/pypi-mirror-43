import setuptools


with open("README.rst", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="pimpygui",
    version="0.1.1",
    author="Philip Schill",
    author_email="philip.schill@gmx.de",
    url="https://gitlab.com/pschill/pimpy",
    description="Graphical user interface for pimpy",
    long_description=long_description,
    python_requires=">=3.6",
    packages=["pimpygui"],
    entry_points={
        "gui_scripts": ["pimpy_gallery = pimpygui.gallery:main"]
    },
    install_requires=[
        "pimpy >= 0.1.0",
        "PySide2 >= 5.12",
    ],
    package_data={
        "pimpygui": ["ui/*.ui"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Artistic Software"
    ]
)
