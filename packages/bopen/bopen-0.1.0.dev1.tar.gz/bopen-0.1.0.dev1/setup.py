import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bopen",
    version="0.1.0.dev1",
    author="Daniel Valenzuela",
    author_email="dowy.vz6@gmail.com",
    description="Open bookmarks from your shell.",
    keywords='sample setuptools development',
    packages=setuptools.find_packages(exclude=['tests*']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanielVZ96/bopen",
    entry_points = {
        'console_scripts': [
            'bopen = bopen.bopen:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    python_requires='>=3',
)
