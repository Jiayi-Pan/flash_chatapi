from setuptools import setup, find_packages

setup(
    name="flash_chatapi",
    version="0.1.0",
    author="Jiayi Pan",
    author_email="i@jiayipan.me",
    description="High-throughput interface for ChatGPT API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jiayi-Pan/flash_chatapi",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["chatgpt"],
    packages=find_packages(),
    install_requires=["aiolimiter", "openai", "tqdm", "aiohttp"],
)
