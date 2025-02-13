from setuptools import setup

setup(
    author='Balázs NÉMETH',
    author_email='balagetech@protonmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPLv3',
        'Operating System :: OS Independent',
    ],
    description='Web application to whatsthedamage written in Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    name='whatsthedamage-web',
    python_requires='>=3.9',
    url='https://github.com/abalage/whatsthedamage-web',
)
