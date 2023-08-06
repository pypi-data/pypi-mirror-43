import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='eic_utils',
      version='0.6',
      description='basic utils :)',
      url='http://github.com/indestinee/utils',
      author='indestinee',
      author_email='indestinee@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
