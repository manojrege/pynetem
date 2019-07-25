import setuptools

setuptools.setup(
    name='pynetem',
    version='0.1',
    author='Manoj R. Rege',
    author_email='rege.manoj@gmail.com',
    url='https://github.com/manojrege/pynetem',
    description='A Python wrapper library for network emulation on MacOS',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: BSD LICENSE",
    ],
    package_data = {'pynetem': ['data/dummynet.conf.j2']},
    include_package_data = True,
)