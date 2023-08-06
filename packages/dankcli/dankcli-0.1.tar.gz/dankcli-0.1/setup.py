from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dankcli',
      version='0.1',
      description='CLI Meme Generator to automatically add whitespace and text to top',
      long_description=readme(),
      keywords='dankcli dank meme memegenerator memes generator pillow dankmemes',
      url='https://github.com/sggts04/dankcli',
      author='Shreyas Gupta',
      author_email='technology.shreyas@gmail.com',
      license='MIT',
      packages=['dankcli'],
      install_requires=[
          'pillow',
      ],
      package_data={
        'dankcli': ['fonts/*.ttf'],
      },
      zip_safe=False)