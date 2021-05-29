from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pyubbink',  
    version='0.1',
    scripts=['pyubbink'] ,
    author="Adam Sillye",
    author_email="adam@berriesand.co",
    description="'Python interface for Ubbink Ubiflux Vigor ventillation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asillye/pyubbink",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
     ],
 )