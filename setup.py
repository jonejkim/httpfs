from setuptools import setup, find_packages

setup(name='httpfs',
    version='0.1',
    author='Jone J Kim',
    author_email='jonejkim@vectors-of-qualia.net',
    url='http://github.com/jonejkim/httpfs',
    description='httpfs - local image/file server with image uploader for typora',
    packages=find_packages(),
    install_requires=[
            'Flask-Reuploaded',
            'markdown',
    ],
    license='MIT',
    zip_safe=False
    )