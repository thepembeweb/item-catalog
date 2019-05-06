# Item Catalog

> "Item Catalog" is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

![](https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg) ![](https://upload.wikimedia.org/wikipedia/commons/9/97/Sqlite-square-icon.svg)

![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)

The app will provide a list of movies within a variety of genres as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own movies.

## Installation

### Requirements
The project uses VirtualBox, Vagrant, Python and SQLite. 

* Install [Python 3](https://www.python.org/downloads/)
* Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Install [Vagrant](https://www.vagrantup.com/downloads.html)

### Setup

* Clone the repo `git clone https://github.com/thepembeweb/item-catalog.git`
* To setup the VM configuration unzip this file: FSND-Virtual-Machine.zip
* Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. 
* Change directory to the vagrant directory with `cd vagrant` 
* Start the virtual machine with `vagrant up`
* Log into the virtual machine with `vagrant ssh`
* Change directory with `cd /vagrant/catalog`
* Load the app with `python app.py`
* Browse to the app in your browser at this URL `http://localhost:8000/`

## Built With

* [Python 3](https://www.python.org/) - The framework used
* [SQLite](https://www.sqlite.org/) - The database used
* [VirtualBox](https://www.virtualbox.org/) - The virtualization software used
* [Vagrant](https://www.vagrantup.com) - The virtual machine environment manager used

## Authors

* **[Pemberai Sweto](https://github.com/thepembeweb)** - *Initial work* - [Item Catalog](https://github.com/thepembeweb/item-catalog)

## License

[![License](http://img.shields.io/:license-mit-green.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
- Copyright 2019 © [Pemberai Sweto](https://github.com/thepembeweb).

