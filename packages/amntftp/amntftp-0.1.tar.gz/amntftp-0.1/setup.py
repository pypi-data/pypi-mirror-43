import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="amntftp",
    version="0.1",
    author="The Munshi Group",
    author_email="support@munshigroup.com",
    description="AmmuNation TFTP protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/munshigroup/amntftp",
    packages=setuptools.find_packages(),
    install_requires = ['lair3','kthread'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
