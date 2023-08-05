# rsyncstats

Parse rsync server logs, compute statistics and store in influxdb.

## Installation

ringserverstats is distributed on PyPI https://pypi.org as a universal wheel.

``` bash
    $ pip install rsyncstats
```

## Influxdb configuration

This program will fill 2 measurements. You should configure a database for these, and configure a user with write priviledges.

### Prepare database

First, create a database, a user, and retention policie.

``` sql
create database rsyncdb
create user rsync with password 'rsyncer'
grant write on rsyncdb to rsync
grant read on rsyncdb to rsync
create retention policy rp_rsyncevents on rsync duration 1w replication 1
create retention policy rp_rsyncstats on rsync duration 520w replication 1
```

## Usage

To work properly, this program needs the following environment variables set :

  * `INFLUXDB_HOST` : The host name or adress of influxdb server
  * `INFLUXDB_PORT` : The port number of influxdb server
  * `INFLUXDB_USER` : The influxdb user to authenticate to
  * `INFLUXDB_PASS` : The password to authenticate with
  * `INFLUXDB_DB`   : The database name containing the metric
  * `INFLUXDB_VERIFY_SSL` : Set to `yes` or `no` to verify SSL connection
  * `INFLUXDB_SSL`  : Should the connection go to https ?

``` bash
$ ringserstats txlogs.log
```

## Explanations

The logs from rsync are metrics suitable for a timeserie database. The idea is to parse the logs, as in the exemple below, and to generate values to insert into an influxdb timeseries database.

The file `grafana-dashboard.json` can be imported into grafana to visualize this timeserie.

Used tags in influxdb :

``` sql
show tag keys from rsyncevents
show tag keys from rsyncstats
```

The rsyncevents measure has several tags :

  * module : the rsync moduled accesed during transfer
  * geohash : location of the client in geohash format
  * hosthash : a hash of the client ip (usefull to correlate the clients requests)
  * city : an english city name

Because storing events in the longterm is not very relevant, the `rsyncstats` measurement groups all events by day, by host and by network. The retention policies discribed above will manage the time your data get stored in influxdb.


## License

`rsyncstats` is distributed under the terms of the GPL v3 or later. See LICENSE file.

## Build

``` shell
python3 setup.py sdist bdist_wheel
```

## Test

``` shell
tox
```
