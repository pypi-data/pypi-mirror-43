import setuptools

setuptools.setup(
    name="monominmono",
    version="0.0.2",
    author="David Whittingham",
    author_email="davidwhittingham94@gmail.com",
    description="A small package that finds a global minimum in ordered arrays, taking advantage of specific monotonicity properties to total number of comparisons in big arrays. Find out more via github, https://github.com/01100100/micropsi",
    long_description_content_type="text/markdown",
    url="https://github.com/01100100/micropsi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
