from pymongo import MongoClient
from os.path import isfile, join
from os import listdir
import pandas as pd


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


def get_data(path):
    data = list()
    json_files = [f for f in listdir(path) if isfile(join(path, f))]

    for json_file in json_files:
        frame_no = int(json_file.split('_')[2])
        json_df = pd.read_json(path + json_file, orient='columns')

        data.append((frame_no, len(json_df['people']), json_df['time_lapse'][0]))

    return data

def read_json(path):
    return pd.DataFrame(get_data(path), columns=['frame_no', 'people', 'time_lapse'])


frames = read_json('../predictions/1/14/openpose/json/2bff565e-3dbd-3a7d-985a-8cf2d3cc1fab/')
mean_time = frames.mean(axis=0)
print(mean_time)
