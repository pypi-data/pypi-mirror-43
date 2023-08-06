import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="recompute",
    version="0.9.7",
    author="Suriyadeepan Ramamoorthy",
    author_email="suriyadeepan.r@gmail.com",
    description="Remote Computation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suriyadeepan/recompute.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
      'console_scripts' : [ 're=recompute.recompute:main' ],
      },
    install_requires=['prettytable==0.7.2', 'pytest==3.3.1']
)
