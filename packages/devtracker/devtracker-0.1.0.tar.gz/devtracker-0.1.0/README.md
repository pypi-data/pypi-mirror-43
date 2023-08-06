# devTracker
*A command line app to easily and efficiently track your time spent working on projects based on the directory you are working in.*


### Basic Set Up

* Ensure you are using python 3.5 or greater by running `python3 --version`.  Get the newest version [here](https://www.python.org/downloads/)
* Make sure you have pip installed and updated as well.  See [docs](https://pip.pypa.io/en/stable/installing/) for more info.
* Run `pip3 install devtracker` and verify successful installation.
* This will install globally and upon first track 'start' a devtrack_projects directory will be created in the current user's home directory to store tracked project's .csv files. (Do not delete or move this directory)

### Alternate Set Up

* Clone Repo into any directory.  Find repo [here](https://github.com/ConSou/devtracker)
* cd into the devtracker directory.
* Ensure you are running python version 3.5 or greater and that you have pip updated.
* Run the install.sh file `./install.sh`. (if you have already installed the project via pip, uninstall before running command.)

### Basic Usage
replace any below `devtracker` command with `dt` as a shortcut

* `cd` into any directory you will be working on.
* Enter `devtracker start`, this will create a .csv file in the a created devtrack_project directory in the current users home folder.  It will log your start time and then exit the program.
* When you are done working on your project enter `devtracker stop` in that same directory and it will add a punch out time and report the total amount of time you have worked in this session.  You can see this in the .csv file.
* Enter `devtracker report` in your working directory to get the total time you have worked in that directory.
* Use flag `--full` after devtracker report to view full .csv file formatted for terminal.
* Use flag `--today` after devtracker report to generate a report for just today's time worked.
* Use flag `--weekly` after devtracker report to generate a weekly report on time worked.
* Add a number after the weekly flag ie. `--weekly x` to determine the number of weeks to report.
* Enter `devtracker status` to check your current time worked or to get report if you have started tracking or not.
* Enter 'devtracker --help' for more information about available arguments and shortcuts.

If you find any issues or would like to submit a feature request please use GitHub's issue tracker, and provide as much detail as possible about
the bug or feature.

run `pip3 uninstall devtracker` if you need/want to uninstall.
Currently devtracker only supports OSX and Linux with python 3.5 or newer.

See CONTRIBUTING.md for more information about setting up project locally to work on bugs or features.

### **Special thanks to our current contributors **

* klaethecoder