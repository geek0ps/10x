from setuptools import setup, find_packages

setup(
    name='pythonOps',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
       "jinja2",
       "pyyaml"
    ],
    # Other metadata
    author='Julius Omoleye',
    author_email='julius.omoleye@outlook.com',
    description='A groundbreaking Python application that simplifies configuration management across multiple platforms, including Terraform, Ansible, and Kubernetes. Write one config file and let PyOps generate the rest!',
    url='https://github.com/AsyncDeveloper245/10x.git',
    
    entry_points={
        'console_scripts': [
            'pyops=PyOps.pyOps:main',
        ],
    },
    
    
    
)
