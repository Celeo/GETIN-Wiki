# GETIN-Wiki

Wiki app from [GETIN-Template](https://github.com/Celeo/GETIN-Template).

## Setup

1. Install Docker and Docker-compose on your system. You don't need Python, Node, or Postgres.
2. Clone down the repo
3. Build the Docker images with `docker-compose build`
4. Copy *config.example.cfg* to *config.cfg* and fill in the fields.

## Development

```bash
$ docker-compose up
```

Open your browser to `http://localhost:8080`. This dev environment runs both Flask and webpack in their debug modes, so changes
you make on your filesystem will be reflected in the running Docker containers.

## Production

Make any necessary changes to the server's configuration.

```bash
$ cd client
$ yarn run build
$ cd ..
$ docker-compose up -f docker-compose.production.yml
```

Open your browser to `http://[server_ip_or_name]`. This prod environment runs the server with Gunicorn and a few workers and uses
Nginx both as a proxy server and a static file server to serve the compiled client files to the user.
