"""An AWS utility package"""
import setuptools
import lambda_logging

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='lambida',  
     version='0.1.01',
     author="AMARO",
     author_email="data@amaro.com",
     description="An AWS utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url=None,
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
