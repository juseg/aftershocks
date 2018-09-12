#!/usr/bin/env python2
# Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Plot JMA recent earthquake magnitudes and frequency by region.
"""

import re
import datetime
import pytz
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def load(region=''):
    """Download latest JMA earthquakes into csv file."""

    # read latest earthquakes list
    url = 'https://www.jma.go.jp/en/quake/quake_singendo_index.html'
    df = pd.read_html(url, header=0, index_col=0)[3]

    # select Iburi region
    df = df[df['Region Name'].str.contains(region, flags=re.IGNORECASE)]

    # save to csv
    df.to_csv('2018-'+region.lower()+'-aftershocks.csv')


def plot(region=''):
    """Plot earthquake magnitude and frequency."""

    # load earthquake data
    df = pd.read_csv('2018-'+region.lower()+'-aftershocks.csv',
                     index_col=0, parse_dates=True)

    # get magnitude and count
    mag = df.Magnitude.str[1:].astype('float32')
    cnt = mag.resample('3H').count().rename('Earthquakes per 3 hour')

    # init figure
    fig, ax = plt.subplots()

    # plot counts
    ax.bar(cnt.index, cnt, alpha=0.75, color='C1', width=0.1)
    ax.grid(True)
    ax.set_ylabel(cnt.name, color='C1')
    ax.set_ylim(0.0, 25.0)
    ax.locator_params(axis='y', nbins=5)
    ax.tick_params(axis='y', colors='C1')

    # plot magnitude
    ax = ax.twinx()
    ax.plot(mag.index, mag, linestyle='', marker='o', alpha=0.75, color='C0')
    ax.set_ylim(2.0, 7.0)
    ax.set_ylabel(mag.name, color='C0')
    ax.locator_params(axis='y', nbins=5)
    ax.tick_params(axis='y', colors='C0')

    # mark main earthquake
    ax.text(mag.index[-1], mag[-1], '  M{:.1f}'.format(mag[-1]), color='C0',
            ha='left', va='center')

    # pretty time ticks
    tz = pytz.timezone('Asia/Tokyo')
    ax.xaxis.set_major_locator(mdates.DayLocator(tz=tz))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('\nSep %d', tz=tz))
    ax.xaxis.set_minor_locator(mdates.HourLocator(range(0, 24, 12), tz=tz))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H', tz=tz))

    # add current time
    now = datetime.datetime.now(tz=tz)
    ax.axvline(now, linestyle='--', color='C3')
    ax.text(now, 5.1, 'updated ' + now.strftime('%H:%M'), color='C3',
            ha='right', va='bottom', rotation=90)

    # add title
    # FIXME replace 2018 by current year
    region = region or 'japan'
    ax.set_title("2018 "+region.title()+" earthquake and aftershocks\n"
                 "Source: Japan Meteorological Agency (www.jma.go.jp)",
                 pad=10.0)

    # save
    fig.savefig('2018-'+region.lower()+'-aftershocks.svg')
    fig.savefig('2018-'+region.lower()+'-aftershocks.png')


if __name__ == '__main__':
    """Main program for command-line execution."""

    import argparse

    # parse arguments(future args: from lang)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--at', default='', metavar='NAME',
                        help='filter by region name (default: Japan)')
    args = parser.parse_args()

    # load data and plot
    load(region=args.at)
    plot(region=args.at)
