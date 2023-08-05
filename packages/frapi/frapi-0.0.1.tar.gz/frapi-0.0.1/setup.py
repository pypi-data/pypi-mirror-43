import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frapi",
    version="0.0.1",
    author="BIG CHENG",
    author_email="bigcheng.asus@gmail.com",
    description="Package for Face Recognition API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BIG-CHENG/FaceRec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
