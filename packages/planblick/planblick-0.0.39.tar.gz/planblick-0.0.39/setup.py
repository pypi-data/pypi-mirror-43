from setuptools import setup
version = "0.0.39"
setup(name='planblick',
      version=version,
      description='',
      url='https://www.planblick.com',
      author='Florian Kröber @ Planblick',
      author_email='fk@planblick.com',
      license='MIT',
      packages=['planblick.httpserver', 'planblick.autorun', 'planblick.sqs', 'planblick.logger'],
      install_requires=[
          'cherrypy',
          'requests',
          'boto3',
      ],
      zip_safe=False)
