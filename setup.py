from setuptools import setup

setup(
    name='pagan',
    packages=['pagan'],
    use_2to3=True,
    include_package_data=True,
    version='0.4.3',
    url='https://github.com/daboth/pagan',
    download_url='https://github.com/daboth/pagan/tarball/0.4.3',
    license='GPL',
    description='python avatar generator for absolute nerds',
    long_description=open('README.md').read(),
    author='David Bothe',
    author_email='davbothe@googlemail.com',
    keywords=['avatar', 'identicon', 'generator'],
    scripts=['tools/console/pagan'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['Pillow>=2.3.0']

)
