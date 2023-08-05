from setuptools import setup, find_packages


setup(
    name='nlp2',
    version='1.5.0',
    description='Tool for NLP - handle file and text',
    long_description="Github : https://github.com/voidful/nlp2",
    url='https://github.com/voidful/nlp2',
    author='Eric Lam',
    author_email='voidful.stack@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='nlp file io string text mining',
    packages=find_packages()
)
