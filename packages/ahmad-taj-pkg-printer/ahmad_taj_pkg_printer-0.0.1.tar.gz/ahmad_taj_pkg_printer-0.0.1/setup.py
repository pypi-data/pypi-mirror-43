import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ahmad_taj_pkg_printer",
    version="0.0.1",
    author="Ahmad Taj",
    author_email="Ahmadtaj77@gmail.com",
    description="A small printer package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ahmadtaj1754",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
