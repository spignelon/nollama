from setuptools import setup, find_packages
import os


def load_requirements(filename):
    """Load requirements from a file."""
    requirements = []
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            requirements = file.read().splitlines()
    return requirements


setup(
    name="nollama",
    version="0.3",
    packages=find_packages(),
    install_requires=load_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "nollama=nollama.nollama:main",
        ],
    },
    description="A terminal-based interface for interacting with large language models (LLMs)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/spignelon/nollama",
    author="Ujjawal Saini",
    author_email="spignelon@proton.me",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
