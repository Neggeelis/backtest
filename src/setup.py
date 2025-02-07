from setuptools import setup, find_packages

setup(
    name="trading_bots_deepseek",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "telegram",
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "talib",
    ],
)