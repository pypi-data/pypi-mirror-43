from setuptools import setup, find_packages

install_requires = ['grpcio-tools==1.18.0',
                    'googleapis-common-protos==1.5.6',
                    'python-daemon==2.2.0',
                    'mysqlclient==1.4.1',
                    'SQLAlchemy==1.2.17',
                    'python-dotenv==0.10.1',
                    'PyYAML==5.1']

setup(
    name='podder-task-base',
    version='0.1.2',
    packages=find_packages(),
    author="podder-ai",
    url='https://github.com/podder-ai/podder-task-base',
    include_package_data=True,
    install_requires=install_requires,
)
