import json
import pandas as pd
import plotly.express as px
import datetime
from zoneinfo import ZoneInfo

def generate_graphs(infilename, outfilename_base):
    f = open(infilename)
    data = json.load(f)
    f.close()

    times = []
    johnjay = []
    jj = []
    ferris = []
    time_fmt = '%Y-%m-%d %H:%M:%S'
    local_tz = ZoneInfo("America/New_York")
    utc_tz = ZoneInfo("UTC")

    for key in data:
        nofrac, frac = key.split('.')
        dt = datetime.datetime.strptime(nofrac, time_fmt)
        dt = dt.replace(tzinfo=utc_tz)
        dt_local = dt.astimezone(local_tz)
        timestr = dt_local.strftime(time_fmt)

        times.append(timestr)
        print(timestr)
        johnjay.append(int(data[key]['155']['client_count']))
        jj.append(int(data[key]['192']['client_count']))
        ferris.append(int(data[key]['103']['client_count']))

    # Calling DataFrame constructor after zipping
    # both lists, with columns specified
    df_johnjay = pd.DataFrame(list(zip(times, johnjay)), columns =['Time', 'John Jay'])
    df_jj = pd.DataFrame(list(zip(times, jj)), columns =['Time', 'JJ'])
    df_ferris = pd.DataFrame(list(zip(times, ferris)), columns =['Time', 'Ferris'])


    fig_johnjay = px.line(df_johnjay, x="Time", y="John Jay", title="Crowd Patterns - John Jay Dining Hall") 
    fig_jj = px.line(df_jj, x="Time", y="JJ", title="Crowd Patterns - JJ's Place") 
    fig_ferris = px.line(df_ferris, x="Time", y="Ferris", title="Crowd Patterns - Ferris Booth Commons") 
    print(outfilename_base)
    fig_johnjay.write_html('{}_{}'.format('johnjay', outfilename_base))
    fig_jj.write_html('{}_{}'.format('jj', outfilename_base))    
    fig_ferris.write_html('{}_{}'.format('ferris', outfilename_base))
