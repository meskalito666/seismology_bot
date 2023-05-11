import json 
import pytz
import requests
from datetime import datetime
from typing import List, Dict
from shapely.geometry import Point, Polygon
from consts import (
    GOOGLE_MAP_URL, GEOCODE_URL, TIMEDIFF_BETWEEN_UPDATES, 
    MAGNITUDE_THRESHOLD, polygon_list)



def check_location(latitude: float, longitude: float, region: str,
                   polygon: List[List[float]]=polygon_list) -> bool:
    """
    to check: \n
      1. if 'ARMENIA' in the name of region
      2. if the earthquake is inside the polygon "around" Armenia
    
    The polygon in this case is a figure outlined by 4 points on the map, 
    including the regions closest to Armenia

    TODO: transform latitude and longitude and use adjusted values to check location
    https://en.wikipedia.org/wiki/Mercator_projection
    https://wiki.gis-lab.info/w/Пересчет_координат_из_Lat/Long_в_проекцию_Меркатора_и_обратно#.D0.9A.D0.BE.D0.B4_.D0.BD.D0.B0_Python
    """
    # check by name
    is_arm = 'ARMENIA' in region.upper()
    # check by coodrinates 
    polygon = Polygon(polygon_list)
    point = Point([latitude, longitude])

    return point.within(polygon) or is_arm


def check_aftershock(info: Dict) -> bool:
    """
    parse time and check timediff between earthquake and aftershock to avoid spam \n
    aftershocks outside of Armenia will be skipped

    info['time'] - time of original earthquake \n
    info['lastupdate'] - time of aftershock \n

    time format from json: 2023-02-13T23:56:22.4Z
    """
    if info['action'] == 'create':  # check if new
        return True
    elif 'ARMENIA' not in info['flynn_region'].upper(): # skip if aftershock is outside of Armenia 
        return False
    else:  # else check timediff between updates
        _time = datetime.strptime(info['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        _lastupdate = datetime.strptime(info['lastupdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
        timediff = abs((_lastupdate - _time).total_seconds())

        return timediff > TIMEDIFF_BETWEEN_UPDATES
    

def check_magnitude(info: Dict, threshold: float=MAGNITUDE_THRESHOLD) -> bool:
    """
    check magnitude to avoid spam
    """
    if 'ARMENIA' in info['flynn_region'].upper(): # anyway show a notification if earthquake in Armenia 
        return True
    elif info['mag'] >= threshold:
        return True
    else:
        return False


def get_map_link(latitude: float, longitude: float) -> str: 

    url = GOOGLE_MAP_URL.format(latitude, longitude)
    Earth_emoji = u'\U0001F30F'
    output_string = f'<a href="{url}">{Earth_emoji}map</a>'

    return output_string


def get_location_name(latitude: float, longitude: float) -> str:

    url = GEOCODE_URL.format(latitude, longitude)
    data = requests.get(url).text
    data = json.loads(data)
    output_string = ''

    if data['countryName']:
        output_string += f"country: #{data['countryName']} \n"

    if data['principalSubdivision']:
        output_string += f"province: {data['principalSubdivision']} \n" 

    if data['city']:
        output_string += f"city: {data['city']} \n" 

    if output_string == '':
        output_string += 'undefined location o_O \n'

    return output_string


def get_local_time() -> str:
    
    armenian_tz = pytz.timezone('Asia/Yerevan')
    local_time = datetime.now(tz=armenian_tz).strftime('%d-%m-%Y, %H:%M')

    return 'time: ' + local_time + '\n'


def prepare_msg_for_tg(latitude: float, longitude: float, info: Dict) -> str:
    # get type of action
    if info['action'] == 'create':
        action = 'New earthquake! \n'
    elif info['action'] == 'update':
        action = 'Aftershock. \n'
    else:
        action = ''
    # get magnitude
    mag = f'magnitude: {info["mag"]} \n'
    # get depth
    depth = f'depth: {info["depth"]} \n'
    # get time from json
    # time = f'time: {info["lastupdate"]} \n'
    # or get local time 
    time = get_local_time()
    # get location
    lacation_name = get_location_name(latitude, longitude)
    # get map link
    map_link = get_map_link(latitude, longitude)

    return action + time + mag + depth + lacation_name + map_link


if __name__ == '__main__':
    # print(check_location(41.548973, 43.190972, '', polygon_list))
    # print(get_location_name(39.145481417814864, 46.135839891752056))
    # info = {
    #     'action':'upd',
    #     'time':'2023-02-14T08:19:24.4Z',
    #     'lastupdate':'2023-02-14T08:25:00.0Z'
    # }
    # print(check_time(info))
    print(get_local_time())

    