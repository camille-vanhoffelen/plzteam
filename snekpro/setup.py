import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "1.0"

requirements = [
    "fastapi",
    "uvicorn",
    "torch",
    "torchvision",
    "tensorflow",
    "ray",
    "atari-py",
    "numpy",
    "matplotlib",
]

setuptools.setup(
    name="snekpro",
    version=version,
    author="snekbros",
    description="Python API for tagpro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
