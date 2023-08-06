from setuptools import setup, find_packages

setup(
    name='requestx',  # Required
    author="Paulo Sergio dos Santo Junior",
    author_email="paulossjuniort@gmail.com",
    description="A wrapper of Requests",
 
    url="https://github.com/paulossjunior/requestx",
 
    version='0.0.8',  # Required
    
    packages=['requestx'],
 
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    setup_requires=['wheel'],
    install_requires=['requests'],  # Optional
)