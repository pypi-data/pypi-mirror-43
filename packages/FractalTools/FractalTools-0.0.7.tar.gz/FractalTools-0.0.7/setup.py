import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FractalTools",
    version="0.0.7",
    author="Blake Brown",
    author_email="author@example.com",
    description="A small package for quickly generating Julia and Mandelbrot sets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Custards1/FractalTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
