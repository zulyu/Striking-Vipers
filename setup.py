from setuptools import setup, find_packages

setup(
    name="striking-vipers",
    version="0.1",
    packages=find_packages(),
    package_data={
        '': ['config.py'],  # Include config.py in the root
    },
    install_requires=[
        'Flask==2.0.1',
        'Flask-RESTX==0.5.1',
        'Flask-SQLAlchemy==2.5.1',
        'SQLAlchemy==1.4.23',
        'PyMySQL==1.0.2',
        'pytest==6.2.5',
        'pytest-cov==2.12.1',
        'gunicorn==20.1.0',
        'python-dotenv==0.19.0',
        'pylint==3.0.3',
        'coverage==6.0.2',
        'pytest-flask==1.2.0',
        'requests==2.26.0',
        'Werkzeug==2.0.1',
        'black==24.3.0',
        'pygame==2.1.2',
        'selenium==4.18.1',
        'webdriver-manager==4.0.1',
        'PyJWT'
    ],
) 