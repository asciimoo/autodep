from setuptools import setup, find_packages

setup(
    name='autodep',
    version='0.0.3',
    author='Adam Tauber',
    author_email='asciimoo@gmail.com',
    description=('Install python dependencies automatically at runtime'),
    license='GPLv3+',
    keywords="dependency installer",
    url='https://github.com/asciimoo/autodep',
    scripts = ['autodep.py'],
    py_modules=['autodep'],
    packages=find_packages(),
    install_requires=['pip', 'charade'],
    download_url='https://github.com/asciimoo/autodep/tarball/master',
    entry_points={
        "console_scripts": ["autodep=autodep:__main__"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
