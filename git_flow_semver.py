#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser
from ConfigParser import ConfigParser
import re
import subprocess
from semantic_version import Version

TargetPath = ''
VersionMatch = ''
VersionString = ''
TargetContents = ''
Verbose = False

def printVerbose(s):
	if Verbose:
		print s
##

def flowStart(action, increment):
	version = Version(VersionString)
	if increment == 'patch':
		version.patch += 1
	elif increment == 'minor':
		version.minor += 1
	elif increment == 'major':
		version.major += 1
	else:
		raise Exception('unexpected increment target')

	newVersionString = "%d.%d.%d" % (version.major, version.minor, version.patch)
	print "running - git flow %s start %d.%d.%d" % (action, version.major, version.minor, version.patch)
	if subprocess.call(['git', 'flow', action, 'start', "%d.%d.%d" % (version.major, version.minor, version.patch)]) != 0:
		sys.exit()

	newContents = TargetContents[:VersionMatch.start(1)] + newVersionString + TargetContents[VersionMatch.end(1):]
	with open(TargetPath, 'w+') as fTarget:
		fTarget.write(newContents)

	subprocess.call(['git', 'add', TargetPath])
##

if __name__ == '__main__':
	argParser = ArgumentParser()
	argParser.add_argument('cmd', choices=['print', 'hotfix', 'release'], nargs='?', default='print')
	argParser.add_argument('inc', choices=['major', 'minor', 'patch'], nargs='?', default='patch')
	argParser.add_argument('-v', '--verbose', action='store_true')
	args = argParser.parse_args()
	
	Verbose = args.verbose
	printVerbose('running in verbose mode')


	SectionName = 'config'
	TargetKey = 'version_file'
	PatternKey = 'version_pattern'
	DefaultTarget = './.version'
	DefaultTargetContents = 'Version = 0.0.0'
	DefaultPattern = 'Version\s*=\s*(\d+.\d+.\d+)'

	cwd = os.getcwd() + '/'
	strConfPath = cwd + '.git_flow_semver'
	printVerbose('using config file on : ' + strConfPath)
	conf = ConfigParser()
	try:
		conf.read(strConfPath)
	except Exception:
		printVerbose('no config file exists')

	if not conf.has_section(SectionName):
		printVerbose('making a new config file with default settings')
		conf.add_section(SectionName)
		conf.set(SectionName, TargetKey, DefaultTarget)
		conf.set(SectionName, PatternKey, DefaultPattern)
		with open(strConfPath, 'w+') as fConf:
			conf.write(fConf)
			printVerbose('config written on :' + strConfPath)
		with open(DefaultTarget, 'w+') as fTarget:
			fTarget.write(DefaultTargetContents)
			printVerbose('version information written on :' + DefaultTarget)
	##

	TargetPath = cwd + conf.get(SectionName, TargetKey)
	strVersionPattern = conf.get(SectionName, PatternKey)

	with open(TargetPath, 'r') as fTarget:
		TargetContents = fTarget.read()
	printVerbose('using version info on : ' + TargetPath)
	VersionMatch = re.search(strVersionPattern, TargetContents)
	VersionString = VersionMatch.group(1)

	if args.cmd == 'print':
		print 'current version : ' + VersionString
	elif args.cmd == 'hotfix':
		flowStart('hotfix', args.inc)
	elif args.cmd == 'release':
		flowStart('release', args.inc)
##
