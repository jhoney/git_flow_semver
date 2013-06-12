git_flow_semver
===============

git flow helper to manage semantic version


Dependency
----------

 * Python2 (>= 2.5)
 * Python semantic_version2

Usage
-----
<pre>
	$ git_flow_semver.py -h
	usage: git_flow_semver.py [-h] [-v]
							  [{print,hotfix,release}] [{major,minor,patch}]

	positional arguments:
	  {print,hotfix,release}
	  {major,minor,patch}

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose
</pre>

 * -h, --help : show help message
 * -v, --verbose : show verbose messages
 * print | hotfix | release : running mode, defalt - print
 * major | minor | patch : version part to increase, defalt - patch

First Run
---------
<pre>
	$ git_flow_semver.py -v
	running in verbose mode
	using config file on : /Users/jhoney/work/.git_flow_semver
	making a new config file with default settings
	config written on :/Users/jhoney/work/.git_flow_semver
	version information written on :./.version
	using version info on : /Users/jhoney/work/./.version
	current version : 0.0.0
</pre>

First run will make default config file and version file.

Open git flow hotfix/release
----------------------------
<pre>
	$ git_flow_semver.py
	current version : 0.0.0

	$ git_flow_semver.py hotfix
	running - git flow hotfix start 0.0.1
	Switched to a new branch 'hotfix/0.0.1'

	Summary of actions:
	- A new branch 'hotfix/0.0.1' was created, based on 'master'
	- You are now on branch 'hotfix/0.0.1'

	Follow-up actions:
	- Bump the version number now!
	- Start committing your hot fixes
	- When done, run:

		 git flow hotfix finish '0.0.1'

	$ git diff --cached --name-only
	.version
</pre>

 * Add git_flow_semver config file and version file to your repository.
 * In a git flow inited work directory, run "git_flow_semver.py hotfix" (or release) to advance version and open new hotfix branch.

Customization
-------------
You can specify your own version file. Please refer to the config file. (.git_flow_semver)
