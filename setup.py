from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="youtube_discussion_tree_api",
    version="1.0.2",
    author="Quim10^-12",
    author_email="quimpm99@gmail.com",
    url="https://github.com/quimpm/youtube_discussion_tree",
    description="This is a python API that allows you to obtain the discussion that occurs in the comments of a YouTube video as a tree structure.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "youtube_transcript_api", "transformers", "torch", "torchvision",  "torchaudio", "treelib", "nltk"],
)