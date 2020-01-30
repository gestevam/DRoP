# DRoP

Detection of Related Solvent Positions: analysis of conserved crystallographic waters on protein structures

# Set up dev environment

1. [Install docker](https://docs.docker.com/install/)
2. Copy
    - `config.php.example` to `config.php`
    - `config.env.example` to `config.env` and change the password to something new and random
2. Run `docker-compose up`
3. Go to http://localhost:8888/ in your browser

To stop the server, use Ctrl-C.

To reset your database (deleting all its contents!) run
`docker-compose rm database`.
