
# Table of Contents

1.  Description
2.  Installation

# Description

This project is an example of an Machine Learning API. In this case
the Machine Learning (ML) model is a sentiment analysis for the spanish
lenguage.

The API is written in **FastAPI** and the ML model that is used is the *Python*
package **sentiment-analysis-spanish**.

# Installation

The API runs in a *docker container*, so the *docker image* is needed.

You can build the development image or the production image depending the
stage you are in. To build the development image use

``` sh
$ ./scripts/start_develop.sh build
```

and for the the production image used

``` sh
$ ./scripts/start.sh build
```

Also, once that the image is already built you just can use

``` sh
$ ./scripts/start.sh
```

to run the API.

If you want to stop the API the command is

``` sh
$ ./scripts/stop.sh
```

Once the API is running you can access the *swagger* documentation from a web
browser in `localhost/docs`.

