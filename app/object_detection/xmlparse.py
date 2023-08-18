from datetime import datetime
from typing import MutableSequence
from xml.etree import ElementTree

from app.schemas import detection_locations as detection_locations_schemas


class XmlPars:
    __tree: ElementTree
    __start_children: int
    __end_children: int
    __locations: ElementTree.Element | MutableSequence[ElementTree.Element] = []

    def __init__(self, xml_path: str):
        self.__tree = ElementTree.parse(xml_path).getroot()
        self.__start_children = 1
        self.__end_children = len(self.__tree)

    @staticmethod
    def change_str_to_datetime(time: str) -> datetime:
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_start_datetime(self) -> datetime:
        return self.change_str_to_datetime(time=self.__tree[1][0].text)

    def __get_closest_index(self, time: datetime) -> int:
        closet_index = 0
        for i in range(len(self.__locations)):
            if abs(self.change_str_to_datetime(self.__locations[closet_index][0].text) - time) > abs(
                    self.change_str_to_datetime(self.__locations[i][0].text) - time):
                closet_index = i

        return closet_index

    def get_current_location(self, time: datetime) -> detection_locations_schemas.DetectionLocationsBase | None:
        self.__locations = self.__tree[self.__start_children:self.__end_children]
        index = self.__get_closest_index(time=time)
        self.__start_children += index

        return detection_locations_schemas.DetectionLocationsBase(latitude=self.__locations[index].get("lat"),
                                                                  longitude=self.__locations[index].get("lon"))

    def get_all_location(self) -> list[detection_locations_schemas.DetectionLocationsBase]:
        location: list[detection_locations_schemas.DetectionLocationsBase] = list()

        for i in self.__tree[1:self.__end_children]:
            location.append(
                detection_locations_schemas.DetectionLocationsBase(latitude=i.get("lat"), longitude=i.get("lon")))

        return location
