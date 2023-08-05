import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-ahmad-taj",
    version="0.0.1",
    author="Ahmad Taj",
    author_email="Ahmadtaj77@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

"""
setup() takes several arguments. This example package uses a relatively minimal set:

name is the distribution name of your package. This can be any name as long as only contains letters, numbers, _ , and -. It also must not already taken on pypi.org. Be sure to update this with your username, as this ensures you won’t run into any name collisions when you upload the package.

version is the package version see PEP 440 for more details on versions.

author and author_email are used to identify the author of the package.

description is a short, one-sentence summary of the package.

long_description is a detailed description of the package. This is shown on the package detail package on the Python Package Index. In this case, the long description is loaded from README.md which is a common pattern.
long_description_content_type tells the index what type of markup is used for the long description. In this case, it’s Markdown.

url is the URL for the homepage of the project. For many projects, this will just be a link to GitHub, GitLab, Bitbucket, or similar code hosting service.

packages is a list of all Python import packages that should be included in the distribution package. Instead of listing each package manually, we can use find_packages() to automatically discover all packages and subpackages. In this case, the list of packages will be example_pkg as that’s the only package present.

classifiers tell the index and pip some additional metadata about your package. In this case, the package is only compatible with Python 3, is licensed under the MIT license, and is OS-independent. You should always include at least which version(s) of Python your package works on, which license your package is available under, and which operating systems your package will work on. For a complete list of classifiers, see https://pypi.org/classifiers/.

"""
