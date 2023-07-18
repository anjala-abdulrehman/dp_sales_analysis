from setuptools import setup, find_packages

setup(
    name='dp_sales_pipeline',
    version='1.0.0',
    description='ETL for retail sales data',
    author='Anjala',
    author_email='anjala.lahan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas==1.3.0',
        'pydantic==1.8.2',
        'email-validator==1.1.3',
        'requests==2.26.0',
        'tenacity'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
