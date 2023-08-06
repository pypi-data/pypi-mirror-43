from setuptools import setup, find_packages

setup(
    name='certify-certbot',
    version='1.0.1',
    packages=find_packages(),
    url='https://github.com/SiLeader/certify',
    license='Apache License 2.0',
    author='SiLeader',
    author_email='sileader.dev@gmail.com',
    description='certbot command wrapper',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "certify = certify.certify.main"
        ]
    },

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
    ]
)
