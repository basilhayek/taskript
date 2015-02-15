# Taskript

Taskript is a Tasker-inspired Python script to trigger certain activities based on time or location.

## Modules
* taskript.py - the main module
* tskript.py - handles detecting context changes (location, date)
* workclock.py - handles tracking of time spent at the office
* timecard.py - handles creation and submission of a time card
* unittest.py - unit tests

## Limitations
* The current version is very much oriented towards handling my primary use case of submitting time cards for work. Refactoring needs to occur to generalize this.

## License
MIT License. Read LICENSE.