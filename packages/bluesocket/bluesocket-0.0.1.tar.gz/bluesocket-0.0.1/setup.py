import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bluesocket",
    version="0.0.1",
    author="Emin Bugra Saral",
    author_email="eminbugrasaral@me.com",
    description="Django Channels logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3megawatt/bluesocket",
    packages=setuptools.find_packages(),
    install_requires=["channels"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)