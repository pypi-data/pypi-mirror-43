import setuptools


setuptools.setup(
    name='flask_url_mapping',
    version='0.5',
    packages=['flask_url_mapping'],
    url='https://github.com/jboegeholz/flaskurls',
    download_url='https://github.com/jboegeholz/flaskurls/archive/0.2.tar.gz',
    license='MIT',
    author='Joern Boegeholz',
    author_email='boegeholz.joern@gmail.com',
    description='Django-style url handling for Flask',
    install_requires=["Flask", "Flask-Login"]
)
