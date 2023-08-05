from setuptools import setup

setup(
    name='cmd_talk',
    version='0.1',
    description=('Command talk component of Hybrid Cloud.'),
    author='newcoderlife',
    author_email='newcoderlife@outlook.com',
    url='https://github.com/newcoderlife/cmd-talk',
    license='MPL-2.0',
    packages=['cmd_talk'],
    entry_points={
        'console_scripts': [
            'cmd_talk=cmd_talk:talk',
            'cmd_talk_serv=cmd_talk:serv'
        ]
    }
)
