import setuptools

with open("pontaria/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pontaria",
    version="0.1.4",
    author="Henrique Cunha",
    author_email="henrique.cunha@birdie.ai",
    description="A time monitoring utility for Birdie's tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    py_modules=['pontaria.auth', 'pontaria.date_utils'],
    include_package_data=True,
    install_requires=['arrow', 'gspread',
                      'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'],
    entry_points={
        'console_scripts': [
            'pontaria = pontaria.app:main'
        ]
    }
)
