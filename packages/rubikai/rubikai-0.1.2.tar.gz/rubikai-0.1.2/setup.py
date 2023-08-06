import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rubikai",
    version="0.1.2",
    author="Forest Agostinelli",
    author_email="agostinelli.f@hotmail.com",
    description="Rubik AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # choose a license
        "Operating System :: OS Independent",
    ),
)
