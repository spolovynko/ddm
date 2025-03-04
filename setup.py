from setuptools import setup, find_packages

setup(
    name="ddm_engine",
    version="0.1.0",
    author="Sergiy Polovynko",
    author_email="sergiy.polovynko@ing.com",
    description="A CLI tool for Dynamic Data Masking.",     
    packages=find_packages(),
    install_requires=[
        "argparse", 
        "presidio-analyzer", 
        "presidio-anonymizer", 
        "pdfplumber",
        "pytesseract",
        "Pillow",
        "opencv-python",
        "PyMuPDF"
    ],
    entry_points={
        "console_scripts": [
            "ddm_engine=dynamic_data_masking.main:main",
        ],
    },
    package_data={
        "dynamic_data_masking.ddm_config.analyzer_config": [
            "all-config-C3.yaml",
            "all-config-C4.yaml",
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
