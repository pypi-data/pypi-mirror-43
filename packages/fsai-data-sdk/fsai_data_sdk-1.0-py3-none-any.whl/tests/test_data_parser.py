# coding: utf-8
import json
from fsai.services.data_object.DynamicObjectData import DynamicObjectData


def test_parse_data_ok():
    with open('./data/trajectories.json') as json_file:
        json_file = json.load(json_file)
        dynamic_object_data = DynamicObjectData.from_json(json_file)
        print('\n')
        sample_object = dynamic_object_data.collections[0].objects[0]
        print(sample_object.get_moving_distance())
        assert sample_object.get_moving_distance() == 4.242640687119286
        assert sample_object.states[0].acceleration.x == -4.656612873077392578e-08
        assert sample_object.states[0].acceleration.y == -9.313225746154785156e-08
        assert sample_object.states[0].acceleration.z == 4.656612873077392578e-08

        assert sample_object.states[0].velocity.x == -12.38638929091393948
        assert sample_object.states[0].velocity.y == 5.039367619901895523
        assert sample_object.states[0].velocity.z == -2.845609406940639019
        assert sample_object.states[0].shape == 'cuboid'
