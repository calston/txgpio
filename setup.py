from setuptools import setup, find_packages


setup(
    name="gpiotest",
    version='0.0.1',
    license='MIT',
    url="http://nowhere",
    description="gpiotest",
    author='Colin Alston',
    author_email='colin@praekelt.com',
    packages=find_packages() + [
        "twisted.plugins",
    ],
    package_data={
        'twisted.plugins': ['twisted/plugins/gpiotest_plugin.py']
    },
    include_package_data=True,
    install_requires=[
        'Twisted',
        'PyYaml',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
