from setuptools import setup, find_packages

setup(
    name='your_project_name',
    version='1.0.0',
    description='A short description of your project',
    author='Your Name',
    author_email='yourname@example.com',
    packages=find_packages(),
    install_requires=[
        'pandas==1.3.0',
        'pydantic==1.8.2',
        'email-validator==1.1.3',
        'requests==2.26.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
