# SudoCool

This is a Django project for an online Sudoku solver.  The name is a very clever pun.


## Development Setup

* run `vagrant up` to provision an Ubuntu VM and run setup script
* login to VM via `vagrant ssh`
* `cd /vagrant`
* start the Django server with `python3 manage.py runserver 0.0.0.0:8000`
* on your host machine, navigate to `localhost:8090`
* once you're done, `vagrant suspend` to the stop the VM
