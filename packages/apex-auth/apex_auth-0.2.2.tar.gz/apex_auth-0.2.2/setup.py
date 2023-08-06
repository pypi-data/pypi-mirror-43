import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="apex_auth",
    version="0.2.2",
    author="Andréas Kühne",
    author_email="andreas.kuhne@promoteint.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promoteinternational/apex-ng-auth",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
