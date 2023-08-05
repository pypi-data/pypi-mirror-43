import setuptools
#from distutils.core import setup, Extension
#from distutils import sysconfig
with open("README.md","r") as fh:
	long_description = fh.read()
setuptools.setup(
    name = 'LabSmith_HVS448x64',
    version='2.0.2dev',
    description='Python x64 support for controlling the LabSmith HVS448',
    author='LabSmith',
    author_email='ecummings@labsmith.com',
    url='http://www.labsmith.com',
    packages=setuptools.find_packages(),#['Python'],
    long_description=long_description,
    long_description_content_type = "text/markdown",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
	"Natural Language :: English",
    ],
  )