# coding: utf-8
import os


from fsai_data_sdk.ForesightDataPortal import ForesightDataPortal

try:
    api_key = os.environ['FORESIGHT_API_KEY']
    secret_key = os.environ['FORESIGHT_SECRET_KEY']
except KeyError:
    raise Exception("FORESIGHT_API_KEY and FORESIGHT_SECRET_KEY environment keys are required to run test")


def test_get_data_all_layers_ok():
    portal = ForesightDataPortal(api_key, secret_key)
    result = portal.get_data_at(lng=-122.1598309, lat=37.4358347, radius=2000, layers=["SEMANTIC_2D", "DYNAMIC_OBJECTS"])
    print(len(result))
    sample_dataset = result[0]
    print(sample_dataset)
    print(sample_dataset.layers.semantic_2d.get())
    print(sample_dataset.layers.dynamic_objects[0].get())
