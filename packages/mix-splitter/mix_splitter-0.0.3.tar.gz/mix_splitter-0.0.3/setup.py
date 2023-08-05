from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mix_splitter',
    version='0.0.3',
    description='Download all the songs in a youtube mix.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alexander Rendón',
    author_email='alexrendon2109@gmail.com',
    license='MIT',
    url="https://github.com/alexdr00/mix_splitter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'mix-splitter=mix_splitter.mix_splitter:main',
        ],
    },
    install_requires=[
        'youtube-dl',
        'beautifulsoup4',
        'fake-useragent',
        'lxml',
        'requests',
    ],
    zip_safe=False
)
