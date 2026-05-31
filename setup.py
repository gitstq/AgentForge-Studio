"""
AgentForge Studio - Setup configuration.
"""

from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().strip().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="agentforge-studio",
    version="1.0.0",
    author="AgentForge Team",
    description="Lightweight terminal AI Agent skill factory and team orchestration engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agentforge/studio",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "tui": ["rich>=13.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentforge=agentforge.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
    ],
)
