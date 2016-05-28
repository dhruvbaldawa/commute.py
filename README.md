# commute.py

This is a helper script for multi-modal commute planning based on the information that you specify.

commute.py helps users who travel across multiple modes of transport
and multiple waypoints to make data-based decisions about which route
to use and prefer at a given time or at a given time in future.

## Table of contents

- [Sample Usage](#sample-usage)
- [Installation](#installation)
- [Configuration](#configuration)
	- [Get the Google API key](#get-the-google-api-key)
	- [Create the configuration file](#create-the-configuration-file)
		- [Sample configuration](#sample-configuration)
		- [Parts of the configuration file](#parts-of-the-configuration-file)
			- [api_key](#apikey)
			- [places](#places)
			- [map](#map)
- [Usage](#usage)
- [Status](#status)

## Sample Usage

```shell
$ commute -c config.yml -s HOME -d WORK
Total time: 26min.
Home (time: 26m. w/traffic drive)
Work
-----
Total time: 43min.
Home (time: 41m. waiting: 02min. bus)
Work
-----
Total time: 45min.
Home (time: 25m. w/traffic drive)
Kwik-e-Mart (time: 20m. w/traffic drive)
Work
-----
  ....
```

## Installation

You can easily install this script using either `pip` or `easy_install`

```shell
$ pip install commute
```

or

```shell
$ easy_install commute
```

## Configuration

### Get the Google API key

This information is borrowed from [Google Maps Python client repo](https://github.com/googlemaps/google-maps-services-python)

Each Google Maps Web Service requires an API key or Client ID. API keys are
freely available with a Google Account at https://developers.google.com/console.
To generate a server key for your project:

 1. Visit https://developers.google.com/console and log in with
    a Google Account.
 1. Select an existing project, or create a new project.
 1. Click **Enable an API**.
 1. Browse for the API, and set its status to "On". The Python Client for Google Maps Services
    accesses the following APIs:
    * Directions API
    * Distance Matrix API
    * Elevation API
    * Geocoding API
    * Time Zone API
    * Roads API
 1. Once you've enabled the APIs, click **Credentials** from the left navigation of the Developer
    Console.
 1. In the "Public API access", click **Create new Key**.
 1. Choose **Server Key**.
 1. If you'd like to restrict requests to a specific IP address, do so now.
 1. Click **Create**.

Your API key should be 40 characters long, and begin with `AIza`.

### Create the configuration file
Then you will need to create a `config.yml` file, or just any `yaml` file with the following key fields

```yaml
api_key:    # your Google API key over here
places:     # all the places which need to be tracked
map:        # the map, or essentially how you commute between any two places
```

#### Sample configuration
```yaml
api_key: AIzaaaaaaaaaaaaaaaaaaaaaaaaaaa

places:
    HOME:
        location: 742, Evergreen Terrace, Springfield
        alias: Home
    WORK:
        location: Springfield Nuclear Power Plant, Springfield
        alias: Work
    KWIK_E_MART:
        location: Kwik-e-Mart, Springfield
        alias: Apu's
    MOES_TAVERN:
        location: Moe's Tavern, Springfield
        alias: Moe's

map:
    HOME:
        KWIK_E_MART:
            - mode: driving
        MOES_TAVERN:
            - mode: driving
            - mode: walking
        WORK:
            - mode: driving
            - mode: transit
              transit_mode: bus
    KWIK_E_MART:
        HOME:
            - mode: driving
        MOES_TAVERN:
            - mode: driving
            - mode: walking
        WORK:
            - mode: driving
    MOES_TAVERN:
        HOME:
            - mode: driving  # drinking and driving is not encouraged
            - mode: walking
        # You don't go to Kwik-e-mart or to work from Moe's
    WORK:
        MOES_TAVERN:
            - mode: driving
```

#### Parts of the configuration file

##### api_key
`api_key` will hold the information about the Google Developer's API key.

##### places
`places` holds information about all the places to be taken under
consideration, and a small description about their physical address
add how to refer to them in the output

Each place has two attributes
    - location: the physical location of the place (the thing you type into Google Maps).
    - alias: an alias to refer by and to use while printing the output.


##### map
`map` key contains all the connections between the places, possible
ways to travel between the places and multiple ways, if any
It can also contain other detailed information about the specific way of travel.

The first nesting under map contains the source, use the identifier from the places key above.

```yaml
map:
    PLACE1:
        PLACE2:
            ....
        ....
    ....
```
The next nesting contains a map of possible destinations from the source, which contains the possible ways to travel from the source to the destination

```yaml
map:
    PLACE1:
        PLACE2:
            - mode: driving
            - mode: transit
            ....
        ....
    ....
```

The routing information supports all the arguments that the Google Maps python client takes. For more information refer to [Google Maps Python API documentation](https://googlemaps.github.io/google-maps-services-python/docs/2.4.3/#module-googlemaps)

## Usage

```shell
$ commute -c config.yml -s HOME -d WORK
$ commute -c config.yml -s HOME -d WORK -w now
$ commute -c config.yml -s HOME -d WORK -w 'in an hour'
$ commute -c config.yml -s HOME -d WORK -w 'friday evening @ 7'
```

The date/time parsing is done with the help of  [parsedatetime](https://github.com/bear/parsedatetime) library, so look at the
 documentation to find more about the formats supported.

For using it as a library,

```python
import time
from commute import get_all_paths, format_path

config_file = "/path/to/config/file"
src = "HOME"
dst = "WORK"
when = time.time()

for rank, path in get_all_paths(config, src, dst, when):
    print(commute.format_path(rank, path))
    print("-" * 5)
```

## Status

This project is at a very early stage right now. Please try it out and report any issues.
