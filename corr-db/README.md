# Cloud of Reproducible Records Database

CoRR is a platform pushing and manipulating records captured
simulation management tools, workflow tools and experimental
devices. This repository holds the model and launches
the database needed for the app. It works in conjunction with
[corr-api](https://github.com/faical-yannick-congo/corr-api),
[corr-cloud](https://github.com/faical-yannick-congo/corr-cloud) and
[corr-view](https://github.com/faical-yannick-congo/corr-view).

## Usage

Use `dbhandle.py` to set up and tear down MongoDB. See

    $ python dbhandle.py --help

for details.

## Testing

Use:

    $ nosetests

## License

[The MIT license.](LICENSE)

## Installation

See the [Docker file](./Dockerfile) for more details.

## Acknowledgment

We would like to acknowledge the tremendous work provided by Dr. Daniel Wheeler
in forging the initial vision of this initiative. His collaboration and
contribution to this project have been critical to this point.