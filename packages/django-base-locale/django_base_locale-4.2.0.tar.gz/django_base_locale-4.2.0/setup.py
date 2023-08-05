from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='django_base_locale',
      version='4.2.0',
      description='Simple way to create multi language Django app.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Maksych/django_base_locale',
      author='Maksym Sichkaruk',
      author_email='maxim.18.08.1997@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['django_base_locale*', 'manage.py']),
      include_package_data=True,
      zip_safe=False)
