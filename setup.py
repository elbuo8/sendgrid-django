from setuptools import setup, find_packages

setup(
    name='sendgrid-django',
    version='1.0.2',
    author='Yamil Asusta',
    author_email='yamil@sendgrid.com',
    url='https://github.com/elbuo8/sendgrid-django',
    packages=find_packages(),
    license='MIT',
    description='SendGrid Backend for Django',
    long_description=open('./README.rst').read(),
    install_requires=["sendgrid==0.5.1"],
)
