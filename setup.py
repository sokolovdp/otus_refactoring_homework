import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="otus_refactoring_homework_sokolovdp",
    version="0.0.1",
    author="Dmitrii Sokolov",
    author_email="sokolovdp@gmail.com",
    description="otus refactoring homework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sokolovdp/otus_refactoring_homework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7.3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu 19.04",
    ],
)