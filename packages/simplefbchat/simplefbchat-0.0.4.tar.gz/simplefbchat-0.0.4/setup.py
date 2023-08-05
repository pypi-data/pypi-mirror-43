import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplefbchat",
    version="0.0.4",
    author="Adam Chyła",
    author_email="adam@chyla.org",
    description="Simple Facebook Chat library for students.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chyla/simplefbchat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fbchat',
    ],
)

