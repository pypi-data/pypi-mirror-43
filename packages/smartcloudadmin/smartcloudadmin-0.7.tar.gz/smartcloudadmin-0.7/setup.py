from setuptools import setup

setup(
    name='smartcloudadmin',
    version='0.7',
    packages=['smartcloudadmin', 'smartcloudadmin.utils', 'smartcloudadmin.models'],
    url='https://github.com/cathaldi/smartcloud-admin-api',
    include_package_data=True,
    license='apache2',
    author='Cathal A. Dinneen',
    install_requires=['requests'],
    author_email='cathal.a.dinneen@gmail.com',
    description=''
)
