__version__ = '0.1.4'

from influxdb import InfluxDBClient
import geohash2
import logging
from geolite2 import geolite2
import click
import re
from typing import List, Dict, Union
from hashlib import sha256
from base64 import b64encode
from datetime import datetime

Event = Dict[str,Union[str, Dict]]

logger = logging.getLogger('rsyncstats')
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def influx_group_query(idbclient: InfluxDBClient, start: int, end: int):
    """
    From a start and end (should be the first and last event in epoch format), make a grouping query to store to a downsampled measurement called rsyncstats
    parameter idbclient must be an instance of InfluxDBClient.
    """
    # check if start < end
    if end < start:
        raise ValueError("Start time (%d) must be before end time (%d)"%(start, end))

    # influxql request :
    query = "select sum(sent) as sent, sum(received) as received, sum(total) as total into rp_rsyncstats.rsyncstats from rp_rsyncevents.rsyncevents where time>=%ds and time<=%ds group by module,hosthash,geohash,city,time(1d) fill(none)"%(start, end)
    logger.debug("Sending grouping query: "+query)
    try:
        result = idbclient.query(query)
        logger.info(("Result: {0}".format(result)))
    except Exception as e:
        logger.error("Error writing group queries to influxdb")
        logger.error(e)

def parse_log(filename: str) -> List[Event]:
    """
    Read a rsync log file and parses information.
    Returns a list of events (dictionary)
    """
    global_pattern = r'(?P<timestamp>20[0-9][0-9] [A-Z][a-z]+\s+[0-9]{1,2}\s+[012][0-9]:[0-5][0-9]:[0-5][0-9])\s+\S+ rsyncd\[(?P<pid>[0-9]+)\]:(?P<logtype>(rsync (to|on)|sent)) ((?P<sentbytes>[0-9]+) bytes\s+received (?P<receivedbytes>[0-9]+) bytes\s+total size (?P<totalbytes>[0-9]+)|(?P<module>[-\w_]+)(?P<directory>\/\S*) from (?P<user>\S+)@(?P<hostname>\S+) \((?P<clientip>\S+)\))'
    georeader = geolite2.reader()
    events = []
    events_buffer = {} # dict of events started but not ended. Key is the PID
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        linecount = 0
        for log in file:
            linecount +=1
            # logger.debug(filename + ":"+str(linecount) +" "+ log)
            event = re.search(global_pattern, log)
            if event == None:
                logger.debug("Ignoring log at %s:%d : %s"%(filename, linecount, log))
                continue
            event_data = event.groupdict()
            # store time as epoch
            event_data['timestamp'] = int(datetime.strptime(re.sub(' +', ' ', event_data['timestamp']), '%Y %b %d %H:%M:%S').timestamp())
            # 2 possible logs are captured by the pattern : connection log and transfer log.
            if event_data['logtype'] == 'rsync to' or event_data['logtype'] == 'rsync on':
                location = georeader.get(event_data['clientip'])
                # hash location and get the city name
                if location != None:
                    event_data['geohash'] = geohash2.encode(location['location']['latitude'], location['location']['longitude'])
                    try:
                        event_data['city'] = location['city']['names']['en']
                    except KeyError:
                        event_data['city'] = ''
                else:
                    logger.warning("No location available at %s:%d : %s\nAssuming it was in Grenoble"%(filename, linecount, log))
                    event_data['geohash'] = 'u0h0fpnzj9ft'
                    event_data['city'] = 'Grenoble'
                # hash hostname
                event_data['hosthash'] = b64encode(sha256(event_data['hostname'].encode()).digest())[:12] # overcomplicated oneliner to hash the hostname
                logger.debug("Storing event in buffer (pid %s)"%(event_data['pid']))
                event_data = {k:event_data[k] for k in event_data if event_data[k] != None}
                events_buffer[event_data['pid']] = event_data
                logger.debug(event_data)
            elif event_data['logtype'] == 'sent':
                event_data['endtime'] = event_data['timestamp']
                # get the data from the events_buffer and merge with what we have
                try:
                    previous_data = events_buffer.pop(event_data['pid'])
                    events.append({ **event_data, **previous_data })
                except KeyError as e:
                    logger.info("Event will not be accounted : "+str(event_data))
    return(events)

def influxdb_send_data(idbclient: InfluxDBClient, data: List[Dict]) -> bool:
    """
    Sends data into influxdb
    """
    try:
        idbclient.write_points(data, time_precision='s', retention_policy='rp_rsyncevents')
    except Exception as e:
        logger.error("Unexpected error writing data to influxdb")
        logger.error(e)
        return False
    return True

@click.command()
@click.option('--influxdbhost',  'dbhost',   help='Influxdb hostname or adress.', envvar='INFLUXDB_HOST')
@click.option('--influxdbport',  'dbport',   help='Influxdb port. Default: 8086', envvar='INFLUXDB_PORT', default=8086, type=click.INT)
@click.option('--influxdbdb',    'dbname',   help='Influxdb database.', envvar='INFLUXDB_DB')
@click.option('--ssl/--no-ssl',              help='Should we connect with SSL ?', default=True, envvar='INFLUXDB_SSL')
@click.option('--verifyssl/--no-verifyssl',  help='Should the connexion do SSL check ?', default=False, envvar='INFLUXDB_VERIFY_SSL')
@click.option('--influxdbuser',  'dbuser',   help='Influxdb user', envvar='INFLUXDB_USER')
@click.option('--influxdbpass',  'password', help='Influxdb pass', envvar='INFLUXDB_PASS')
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def cli(dbhost: str, dbport: int, dbname: str, verifyssl: bool, dbuser: str, password: str, ssl: bool, files: List):
    for f in files:
        influxdb_json_data = []
        logger.info("Opening file %s"%(f))
        # Parsing events from a logfile
        lastevent_time = 0
        firstevent_time = 0
        for event in  parse_log(f):
            # get the first event time
            if firstevent_time == 0 or firstevent_time > event['timestamp']:
                firstevent_time = event['timestamp']
            # get the last event time
            if lastevent_time == 0 or lastevent_time < event['timestamp']:
                lastevent_time = event['timestamp']
            # Constructing an influxdb data from the event
            logger.debug(event)
            influxdb_json_data.append(
                {"measurement": 'rsyncevents',
                 "tags": {
                     "module": event['module'],
                     "geohash": event['geohash'],
                     "city":    event['city'],
                     "hosthash": event['hosthash']
                 },
                 "time": event['endtime'],
                 "fields": {
                     "sent": int(event['sentbytes']),
                     "received": int(event['receivedbytes']),
                     "total": int(event['totalbytes'])
                 }
                }
            )

        if dbhost != None :
            logger.info("Sending %d metrics"%len(influxdb_json_data))

            try:
                logger.debug("host     = "+dbhost)
                logger.debug("database = "+dbname)
                logger.debug("username = "+dbuser)
                client = InfluxDBClient(host     = dbhost,
                                        port     = dbport,
                                        database = dbname,
                                        username = dbuser,
                                        password = password,
                                        ssl      = ssl,
                                        verify_ssl = verifyssl
                )
                i=0
                j=10000
                while j < len(influxdb_json_data) or i==0:
                    logger.info("%d/%d"%(j,len(influxdb_json_data)))
                    influxdb_send_data(client, influxdb_json_data[i:j])
                    i=j
                    j+=10000
                # Now lets group those events in statistics
                influx_group_query(client, firstevent_time, lastevent_time)
                client.close()
            except Exception as e:
                logger.error("Error writing to influxdb %s:%d database %s"%(dbhost,dbport,dbname))
                logger.error(e)
