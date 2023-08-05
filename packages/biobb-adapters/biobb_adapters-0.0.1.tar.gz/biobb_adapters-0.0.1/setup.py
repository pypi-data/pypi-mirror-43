from subprocess import check_call
import setuptools
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        check_call("jupyter-nbextension enable nglview --py --sys-prefix".split())
        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_adapters",
    version="0.0.1",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="Biobb_adapters is the Biobb module collection to use the building blocks with several workflow managers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_adapters",
    project_urls={
        "Documentation": "http://biobb_adapters.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test',]),
    include_package_data=True,
    zip_safe=False,
    install_requires=['jupyter', 'nglview', 'cwltool'],
    python_requires='>=3',
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
