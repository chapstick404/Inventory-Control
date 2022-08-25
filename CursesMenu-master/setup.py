import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CursesMenu", # Replace with your own username
    version="0.0.1",
    author="scoutchorton",
    author_email="scoutchorton@gmail.com",
    description="A GTK inspired widget engine using curses for use with command line interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scoutchorton/CursesMenu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses"
    ],
    python_requires='>=3.6',
)
