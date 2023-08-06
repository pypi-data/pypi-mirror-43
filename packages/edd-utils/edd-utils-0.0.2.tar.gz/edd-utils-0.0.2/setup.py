import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edd-utils",
    version="0.0.2",
    author="Zak Costello",
    author_email="zak.costello@lbl.gov",
    description="Download Studies from an Experiment Data Depot Instance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBEI/edd-utils",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['export_edd_study=edd_utils:commandline_export'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)