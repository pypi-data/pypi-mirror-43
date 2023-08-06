import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="client-scaledinference",
    version="1.0.1",
    author="Scaled Inference",
    author_email="dev.opera@scaledinference.com",
    description="Amp Python Thin Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScaledInference/amp-python-thin",
    packages=['si'],
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
