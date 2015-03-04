# Taskript

Taskript is a Tasker-inspired Python script to trigger certain activities based on time or location.

## Modules

### Core Modules
* tskript.py - the core module which handles detecting context changes (location, date)

### Application-specific Modules
* taskript.py - the main module, which in this case invokes a workclock to handle the context returned by tskript
* workclock.py - handles tracking of time spent at the office
* timecard.py - handles creation and submission of a time card

### Unit Test Modules
* ut_tskript.py - unit tests for tskript module
* ut_workclock.py - unit tests for workclock module

## Limitations
* Needs more examples, instructions, and further development of contexts

## License
MIT License. Read LICENSE.