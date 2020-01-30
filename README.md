# DRoP

Detection of Related Solvent Positions: analysis of conserved crystallographic waters on protein structures

# Set up dev environment

1. [Install docker](https://docs.docker.com/install/)
2. Make sure you have [git](https://git-scm.com/) installed and run
    - `git clone https://github.com/mattoslab/DRoP.git`
    - `cd DRoP`
    - `cp -n config.php.example config.php`
    - `cp -n config.env.example config.env`
    - Open `config.env` and change the password to something new and random
3. Run `docker-compose up`
4. Go to http://localhost:8888/ in your browser

To stop the local server, use Ctrl-C.

To reset your database (deleting all its contents!) run
`docker-compose rm database`.
