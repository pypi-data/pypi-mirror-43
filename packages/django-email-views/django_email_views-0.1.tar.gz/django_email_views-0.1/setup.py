from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='django_email_views',
    version='0.1',
    author='Anatoly Gusev',
    author_email='gusev.tolia@yandex.ru',
    description='Usage ideology Django views for e-mails',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    url='http://localhost:8000',
    packages=find_packages(),
    install_requires=[
        'django',
    ]
)
