from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

# REQUIREMENTS=open("requirements.txt").read().splitlines()

setup(
    name="resource_it",
    version="0.0.1",
    url="https://example.com",
    license="MIT",
    author="Mikalai Davydznka",
    author_email="mikalai.davydzenka@gmail.com",
    description=(
        "Handy wrappers for work with\n"
        "Files, Templates, Remote Repositories and many other RESOURCES"),
    packages=find_packages("src", exclude=("tests", )),
    package_dir={"": "src"},

    # install_requires=REQUIREMENTS,
    install_requires=["pyyaml", "python-consul", "faker", "jinja2"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
