import setuptools
import subprocess
import sys
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Customized setuptools install command - installs fastai with --no-deps"""
    def run(self):
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--no-deps', '{0}=={1}'.format('fastai', '1.0.50.post1')])
        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    cmdclass={
        'install': CustomInstallCommand,
    },
    name="inltk",
    version="0.0.4",
    author="Gaurav",
    author_email="contactgauravforwork@gmail.com",
    description="NLTK for Indian Languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goru001/inltk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    dependency_links=[
        'http://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl'
    ],
    install_requires=[
        'aiohttp>=3.5.4',
        'async-timeout>=3.0.1',
        "Pillow",
        "beautifulsoup4",
        "bottleneck",
        "dataclasses;python_version<'3.7'",
        "fastprogress>=0.1.19",
        "matplotlib",
        "numexpr",
        "numpy>=1.15",
        "nvidia-ml-py3",
        "packaging",
        "pandas",
        "pynvx>=1.0.0;platform_system=='Darwin'",
        "pyyaml",
        "requests",
        "scipy",
        "spacy>=2.0.18",
        "typing"
    ],
)
