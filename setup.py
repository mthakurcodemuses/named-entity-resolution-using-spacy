from setuptools import setup, find_packages

setup(
    name="data_ingestion",
    version="0.0.1",
    author="Manish Thakur",
    description="Python Multiprocessing Module Usage",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ingestdata=app.data_ingestion.data_ingestor:main"
        ]
    },
    install_requires=[
        "spacy==3.5.0",
        "spacy-lookups-data==0.3.2"
    ],
    extras_require={
        "dev": [
            "pytest==5.4.3",
        ]
    }
)
