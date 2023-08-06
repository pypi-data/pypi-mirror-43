import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aliyun-rds-bkp",
    version="0.1.0",
    author="Bill Guo",
    author_email="billguo.feather@outlook.com",
    description="A small tool to download db files \
    from Aliyun RDS per schedule",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/life-game-player/aliyun-rds-bkp",
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=[
        'aliyun-python-sdk>=2.3.2'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
