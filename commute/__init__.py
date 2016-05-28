# coding: utf-8
"""
The MIT License (MIT)

Copyright (c) 2016 Dhruv Baldawa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import networkx as nx
import googlemaps
import time
import math
import yaml


config = {}


def get_alias(key):
    return config['places'][key]['alias']


def get_location(key):
    return config['places'][key]['location']


def build_graph(options):
    g = nx.MultiDiGraph()
    g.add_nodes_from(options.keys())

    for source, possible_destinations in options.iteritems():
        if possible_destinations is None:
            continue
        for destination, routes in possible_destinations.iteritems():
            for route in routes:
                data = route
                g.add_edge(source, destination, **data)
    return g


def has_visited_already(node, path):
    for segment in path:
        if segment['source'] == node:
            return True
    return False


def find_all_paths(G, client, source, destination, start_time,
                   path=None, path_info=None):
    _path = path if path is not None else []
    if path_info is not None:
        _path += [path_info, ]

    if source == destination:
        yield _path
    if source not in G.node:
        yield []

    for start, end, idx, data in G.out_edges_iter(source, keys=True,
                                                  data=True):
        if not has_visited_already(end, _path):
            meta = {
                'source': start,
                'destination': end,
            }
            try:
                r = client.directions(get_location(start),
                                      get_location(end), region="in",
                                      departure_time=start_time, **data)[0]['legs'][0]
            except IndexError:
                # means that the route is not available at the time
                print start, end, meta
                G.remove_edge(start, end, idx)
                continue

            meta.update(data)
            if 'duration_in_traffic' in r:
                meta['duration'] = r['duration_in_traffic']['value']
                meta['traffic'] = True
            else:
                meta['duration'] = r['duration']['value']

            if 'departure_time' in r:
                meta['departure_time'] = r['departure_time']['value']
                meta['waiting_time'] = meta['departure_time'] - start_time
                meta['duration'] += meta['waiting_time']
            new_paths = find_all_paths(G, client, end, destination,
                                       start_time + meta['duration'],
                                       _path[:], meta)
            for new_path in new_paths:
                yield new_path


def seconds_to_minutes(duration):
    return int(math.ceil(duration / 60))


def format_path(rank, path):
    outstr = ["Total time: {:02d}min.".format(seconds_to_minutes(rank))]
    destination = None
    for segment in path:
        s = "{}".format(get_alias(segment['source']))
        s += " (time: {:02d}m.".format(seconds_to_minutes(
            segment['duration']))

        if 'traffic' in segment:
            s += " w/traffic"

        if 'waiting_time' in segment:
            s += " waiting: {:02d}min.".format(
                seconds_to_minutes(segment['waiting_time']))

        if segment['mode'] == "driving":
            s += ' drive'
        elif segment['mode'] == "walking":
            s += ' walk'
        elif segment['mode'] == "transit":
            if segment['transit_mode'] == "rail":
                s += ' rail'
            elif segment['transit_mode'] == "bus":
                s += ' bus'
        destination = get_alias(segment['destination'])
        s += ")"
        outstr.append(s)

    if destination is not None:
        outstr.append("{}".format(destination))
    return "\n".join(outstr)


def path_rank(path):
    return sum(segment['duration'] for segment in path)


def get_all_paths(config_file, src, dst, when=None):
    with open(config_file) as f:
        global config
        config = yaml.load(f.read())

    if src not in config['places'] or dst not in config['places']:
        raise Exception("source or destination are not valid")

    if when is None:
        when = int(time.time())

    client = googlemaps.Client(key=config['api_key'])
    g = build_graph(config['map'])
    return sorted(((path_rank(path), path)
                   for path in find_all_paths(g, client,
                                              src, dst,
                                              when)),
                  key=lambda x: x[0])
