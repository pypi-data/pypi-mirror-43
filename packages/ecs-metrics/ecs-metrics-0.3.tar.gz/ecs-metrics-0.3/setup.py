 
from setuptools import setup

setup(
  name = 'ecs-metrics',         # How you named your package folder (MyLib)
  packages = ['ECSMetrics'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Gives detailed overview of user activities', # Give a short description about your library
  #long_description = 'As a security best practice, AWS recommends that users periodically regenerate their AWS access keys. This tool simplifies the rotation of access keys for any user. \n \n INSTRUCTIONS:\n 1) Before running, create text files and list the user names that have to be blacklisted and whitelisted respectively.\n 2) Type "awsrotate" to run the script.\n' ,
  #long_description_content_type = "text/markdown",
  author = 'Kanishk Saxena',                   # Type in your name
  author_email = 'kanishk.saxena@cred.club',      # Type in your E-Mail
  #scripts=['awsrotatekey/awsrotatekeystart'],
  entry_points={'console_scripts':['ecs-metrics = ECSMetrics.__main__:main']},
  #url = 'https://github.com/saxenakanishk/Intern-Kanishk',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ECS', 'Logs', 'CloudWatch'],   # Keywords that define your package best
  install_requires=[
          'Click',            # I get to this in a second
          'datetime'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',      #Specify which pyhton versions that you want to support
  ],
)