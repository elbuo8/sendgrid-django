from setuptools import setup, find_packages

__version__ = None
with open('sgbackend/version.py') as f:
    exec(f.read())

setup(
    name='sendgrid-django',
    version=str(__version__),
    author='Yamil Asusta',
    author_email='yamil@sendgrid.com',
    url='https://github.com/elbuo8/sendgrid-django',
    packages=find_packages(),
    license='MIT',
    description='SendGrid Backend for Django',
    long_description=open('./README.rst').read(),
    install_requires=[
        "python_http_client >= 2.1.*, <2.3",
        "sendgrid >= 3.5, <4",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
