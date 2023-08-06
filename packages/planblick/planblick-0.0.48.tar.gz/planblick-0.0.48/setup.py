from setuptools import setup
version = "0.0.48"
setup(name='planblick',
      version=version,
      description='',
      url='https://www.planblick.com',
      author='Florian Kröber @ Planblick',
      author_email='fk@planblick.com',
      license='MIT',
      packages=['planblick.httpserver', 'planblick.autorun', 'planblick.sqs', 'planblick.sns', 'planblick.logger'],
      install_requires=[
          'cherrypy',
          'requests',
          'boto3',
          'cryptography',
      ],
      zip_safe=False)
