.. Copyright (c) 2018, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
.. GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

Aftershocks
===========

A small script to plot recent earthquake magnitudes and frequency in Japan by
region, using the Japan Meteorological Agency website_. Used to track
aftershocks of the 2018 Iburi earthquake_.

Requires matplotlib_ and pandas_.

Installation::

   pip install aftershocks

Example usage::

   aftershocks.py --at iburi
   aftershocks.py --help

.. _earthquake: https://en.wikipedia.org/wiki/2018_Hokkaido_Eastern_Iburi_earthquake
.. _matplotlib: https://matplotlib.org
.. _pandas: https://pandas.pydata.org
.. _website: https://www.jma.go.jp
