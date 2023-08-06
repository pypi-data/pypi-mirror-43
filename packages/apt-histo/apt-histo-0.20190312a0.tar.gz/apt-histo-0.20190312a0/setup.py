import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read()

setuptools.setup(
    keywords = ['apt','history'],
    name="apt-histo",
    version=version,
    author="will",
    author_email="will_tam@club-internet.fr",
    description="Read /var/log/apt/history.log.* and display it usefully",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/will_tam-bash/apt-histo.git",
    packages=setuptools.find_packages(),
    license="GNU v3",
    license_files="LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Archiving :: Packaging",
    ],
)
