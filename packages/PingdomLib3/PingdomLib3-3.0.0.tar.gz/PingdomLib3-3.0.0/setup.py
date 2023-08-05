from setuptools import setup

setup(
    name='PingdomLib3',
    version='3.0.0',
    author='Mario Mann',
    author_email='dedi-extern@novatec-gmbh.de',
    packages=['pingdomlib'],
    url='https://github.com/NovaTec-APM/PingdomLib',
    license='ISC license',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Topic :: System :: Monitoring'],
    description='A documented python library to consume the full pingdom API',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.2.1"
    ],
)
