import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

os.environ['SLUGIFY_USES_TEXT_UNIDECODE'] = 'yes'

setup(name='airflow-extended-metrics',
      version='0.1.1',
      description='Package to expand Airflow for custom metrics.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/nytm/airflow-extended-metrics',
      author='Sarah Duncan',
      author_email='sarah.duncan@nytimes.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'tzlocal<2.0.0.0,>=1.5.0.0',  # avoids "error: tzlocal 2.0.0b1 is installed but tzlocal<2.0.0.0,>=1.5.0.0 is required by {'pendulum'}"
          'apache-airflow==1.10.1',  # 1.10.0 has a version conflict "error: Flask-Login 0.2.11 is installed but Flask-Login<0.5,>=0.3 is required by {'flask-appbuilder'}"
          'google-cloud-monitoring==0.31.1'  # for extended logging
      ],
      entry_points={
          'airflow.plugins': [
              'metrics = extensions.monitoring_operators:AirflowMetricPlugin',
          ]
      }
    )
