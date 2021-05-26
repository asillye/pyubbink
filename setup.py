import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='pyubbink',  
     version='0.1',
     scripts=['pyubbink'] ,
     author="Adam Sillye",
     author_email="adam@berriesand.co",
     description="An unofficial Ubbink Ubiflux Vigor modbus package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/asillye/pyubbink",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )