from setuptools import setup, find_packages

setup(
    name="iotile_support_lib_controller_3",
    packages=find_packages(include=["iotile_support_lib_controller_3.*", "iotile_support_lib_controller_3"]),
    version="3.7.15a1",
    install_requires=[u'pyparsing>=2.2.1', u'typedargs>=0.13.2'],
    entry_points={'iotile.proxy_plugin': ['configmanager = iotile_support_lib_controller_3.configmanager', 'sensorgraph = iotile_support_lib_controller_3.sensorgraph', 'controllertest = iotile_support_lib_controller_3.controllertest', 'remotebridge = iotile_support_lib_controller_3.remotebridge', 'tilemanager = iotile_support_lib_controller_3.tilemanager'], 'iotile.type_package': ['lib_controller_types = iotile_support_lib_controller_3.lib_controller_types']},
    author="Arch",
    author_email="info@arch-iot.com"
)