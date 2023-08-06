import setuptools

with open("README.md.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demoApp",
    version="0.0.3",
    author="Madhumitha",
    author_email="madhu@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
