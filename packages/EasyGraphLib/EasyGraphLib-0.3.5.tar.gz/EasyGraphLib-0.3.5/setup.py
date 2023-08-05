import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='EasyGraphLib',
    version='0.3.5',
    description='Python library for creating graphs, trees, and gemini structures.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    packages=setuptools.find_packages(),
    author='Ilya Baranov',
    author_email='logotipick@gmail.com',
    keywords=['Graph', 'Modeling', 'Structures'],
    download_url='https://gitlab.com/AdamFull/easygraphlib/blob/master/dist/EasyGraphLib-0.3.0-py3-none-any.whl',
    url='https://gitlab.com/AdamFull/easygraphlib',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)