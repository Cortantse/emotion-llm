from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="emotionalllm",
    version="0.1.0",
    author="EmotionalLLM Contributors",
    author_email="example@example.com",
    description="基于情感分析的大型语言模型项目",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/emotionalllm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
) 