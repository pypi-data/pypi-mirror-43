import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Lenovo-Ai-Client",
    version="0.0.1",
    author="Chen jie",
    author_email="chenjie_222@163.com",
    description="A Lenovo SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenjie222/ai_client",
    packages=setuptools.find_packages(),
    license='Apache License',
    install_requires=[
        'requests',
        'simplejson',
        'opencv-python',
        'jsonpath'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
