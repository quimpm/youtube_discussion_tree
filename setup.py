from setuptools import setup, find_packages

setup(
    name="youtube_discusion_tree_api",
    version="0.0.1",
    author="Quim10^-12",
    author_email="quimpm99@gmail.com",
    url="https://github.com/quimpm",
    description="This is a python API that allows you to obtain the discusion that occurs on the comments of a Youtube video as a tree structure. It also controls the quota usage that consumes your implementation over Youtube Data Api through this library, and allows you to represent and serialize the discusion tree.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["timechecker = src.main:main"]},
)