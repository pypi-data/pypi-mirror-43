import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mh",
    version="0.0.17",
    author="Mark Hallett",
    author_email="mh@markhallett.co.uk",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markhallett/mh",
    packages=setuptools.find_packages(),
    scripts=['mh.py','code/eg.py','code/l2/l2.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
