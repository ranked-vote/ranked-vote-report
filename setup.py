#!/usr/bin/env python

from setuptools import setup

setup(name='ranked-vote-report',
      version='0.0.1',
      description='Tool for generating reports from a corpus of ranked-vote data.',
      author='Paul Butler',
      author_email='rcv@paulbutler.org',
      url='https://github.com/ranked-vote/ranked-vote-report',
      packages=['ranked_vote_report'],
      entry_points={
          'console_scripts': [
              'rcv-report = ranked_vote_report.bin.generate_reports:main'
          ]
      },
      install_requires=[
          'ranked-vote>=0.0.1',
          'ranked-vote-import>=0.0.1'
      ],
      python_requires='>=3.6',
      )
