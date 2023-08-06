import setuptools

with open("README.md", "r") as readme:
    long_desc = readme.read()

setuptools.setup(
    name="qbs",
    version="1.0.0",
    author="Nonny Moose",
    author_email="moosenonny10@gmail.com",
    description="Quick (and dirty) build system",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nonnymoose/qbs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": [
            "qbs = qbs:main"
        ]
    },
    package_data={"qbs": ["conf/default_config.json"]},
    include_package_data=True
)
