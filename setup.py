from setuptools import setup, find_packages

setup(
    name="trading_bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "aiohttp",
        "pandas",
        "matplotlib",
        "numpy",
        "pytest",
        "ccxt",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "trading_bot = main:main",  # Palaid ar `trading_bot` komandu
        ],
    },
)
