import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantrt-aburke",
    version="0.0.1",
    author="Arthur Burke",
    author_email="amb556@cornell.edu",
    description="A real time quantitative trading python framework for coimnbase pro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ardieb/quantrt",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)