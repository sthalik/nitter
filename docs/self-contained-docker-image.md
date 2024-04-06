### Self-contained docker image for Nitter
In addition to the [regular Nitter docker image](https://github.com/sekai-soft/nitter/pkgs/container/nitter) (plus some minor improvements), this repo also contains the source code and [docker image](https://github.com/sekai-soft/nitter/pkgs/container/nitter-self-contained) for a self-contained wrapper variant of Nitter that makes it easier to customize and run, especially in a PaaS, e.g. the fly.io setup is based on it.

#### Features
* Authenticate with a burner/temporary Twitter account using environment variables
* Customize the instance using using environment variables
* Built-in optional nginx and Redis
    * Nginx with password-protection is included to block malicious scrapers.
    * Redis is included in case some PaaS does not have Redis capability/charge additionally for Redis despite having a free tier.

#### How to use
* The docker image is `ghcr.io/sekai-soft/nitter-self-contained:latest`
* You should sign up and use a burner/temporary Twitter account with 2FA disabled.
* You need a volume mapping into the container path `/nitter-data`
    * This is regardless whether you wish to enable Redis. The volume is needed to persist Twitter authetication info even if Redis is disabled.
* Specify environment variables

| Key                      | Required | Comment                                                                                                                                                                            |
| ------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NITTER_ACCOUNTS_FILE     | Yes      | `/nitter-data/guest_accounts.json`                                                                                                                                                 |
| TWITTER_USERNAME         | Yes      | Burner Twitter account username                                                                                                                                                    |
| TWITTER_PASSWORD         | Yes      | Burner Twitter account password                                                                                                                                                    |
| DISABLE_REDIS            | No       | Use `1` to disable the built-in Redis. You should ensure an external Redis instance is ready to connect before launching the container                                             |
| REDIS_HOST               | No       | Hostname for the Redis instance to connect to. Probably required if using an external Redis instance. Defaults to `localhost`.                                                     |
| REDIS_PORT               | No       | Port for the Redis instance to connect to. Probably required if using an external Redis instance. Defaults to `6379`.                                                              |
| REDIS_PASSWORD           | No       | Password for the Redis instance to connect to. Probably required if using an external Redis instance. Defaults to empty string.                                                    |
| DISABLE_NGINX            | No       | Use `1` to disable the built-in Nginx. **Strongly discouraged if the container is exposed to the Internet.**                                                                       |
| INSTANCE_RSS_PASSWORD    | No       | If the built-in Nginx is not disabled, required password used to protect all `/rss` paths. In order to access them you need to specify a `.../rss?key=<password>` query parameter. |
| INSTANCE_WEB_USERNAME    | No       | If the built-in Nginx is not disabled, required basic auth username to protect all non-rss web UIs.                                                                                |
| INSTANCE_WEB_PASSWORD    | No       | If the built-in Nginx is not disabled, required basic auth password to protect all non-rss web UIs.                                                                                |
| INSTANCE_BASE64_MEDIA    | No       | Use `1` to enable base64-encoded media.                                                                                                                                            |
| PORT                     | No       | Port that your Nitter instance binds to. Default to `8080`                                                                                                                         |
| INSTANCE_TITLE           | No       | Name of your Nitter instance shown on the web UI. Defaults to `My Nitter instance`.                                                                                                |
| INSTANCE_THEME           | No       | Default theme of the web UI. Available options are `Black`, `Dracula`, `Mastodon`, `Nitter`, `Pleroma`, `Twitter` and `Twitter Dark`. Defaults to `Nitter`.                        |
| INSTANCE_INFINITE_SCROLL | No       | Use `1` to enable infinite scrolling. Enabling this option will load Javascript on the web UI.                                                                                     |
| INSTANCE_HOSTNAME        | No       | The hostname used to render public-facing URLs such as hyperlinks in RSS feeds. Defaults to `localhost:8080`.                                                                      |

* After the container is up, Nitter is available at port 8081 within the container if Nginx is enabled, and at port 8080 within the container if Nginx is disabled.

#### Some inner working details
* Multiple processes are orchestrated by [`overmind`](https://github.com/DarthSim/overmind)
* `/src/scripts/dump_env_and_procfile.sh` was needed before `overmind` can execute
    * `dump_env_and_procfile.sh` writes the `Procfile` of course
    * `dump_env_and_procfile.sh` also writes expected environment variables to `.env` because `overmind` does not seem to inherit environment so [it had to be an `.env` file](https://github.com/DarthSim/overmind?tab=readme-ov-file#overmind-environment)