import setuptools

setuptools.setup(
    name='pyvjoy',
    version='1.0.0',
    description='Python bindings for vJoy',
    url='https://github.com/maxofbritton/pyvjoy',
    packages=setuptools.find_packages(),
    package_data={'': ['utils/*/*.dll']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ]
)