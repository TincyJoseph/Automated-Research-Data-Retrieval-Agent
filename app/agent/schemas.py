from typing import List
from dataclasses import dataclass
from pydantic import BaseModel, Field



# ===================== RESPONSE SCHEMA =====================

class PlaceInfo(BaseModel):
    name: str=Field(description="Name of the particular tourist spot")
    attraction: str=Field(description="Main attractions or highlights")
    how_to_reach: str=Field(description="How to reach the spot")

class HotelsInfo(BaseModel):
    hotels_nearby: List[str]=Field( description="List of hotels available near the destination")

class TravelResponse(BaseModel):
    tourist_place: str=Field(description="Main tourist destination requested")
    places: List[PlaceInfo]= Field(description="Important places to visit inside the destination")
    hotels: HotelsInfo
    how_to_reach:str=Field(description="How to reach the main destination")
