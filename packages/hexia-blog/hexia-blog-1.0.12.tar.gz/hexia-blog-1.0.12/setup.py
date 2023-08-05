import os
from setuptools import find_packages, setup
from blog import get_version
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='hexia-blog',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django Blog app.',
    keywords='django blog app',
    long_description=README,
    url='https://github.com/HenryMehta/hexia-blog',
    author='Henry Mehta',
    author_email='hjsmehta@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['django-ckeditor'],
    python_requires='>=3',
)
