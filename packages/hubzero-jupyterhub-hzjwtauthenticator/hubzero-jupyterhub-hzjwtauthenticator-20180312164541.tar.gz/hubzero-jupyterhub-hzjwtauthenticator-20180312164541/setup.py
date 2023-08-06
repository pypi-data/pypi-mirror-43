from setuptools import setup

setup(
    name='hubzero-jupyterhub-hzjwtauthenticator',
    version='20180312164541',
    description='JSONWebToken Authenticator for JupyterHub, based on mogthesprog/jwtauthenticator',
    url='https://github.com/hubzero/jwtauthenticator.git',
    author='David Benham',
    author_email='david.r.benham@gmail.com',
    license='Apache 2.0',
    packages=['hzjwtauthenticator'],
    install_requires=[
        'jupyterhub',
        'python-jose',
    ]
)
