""" utils module tests """
from kafkaconnectsync.utils import isjsonequal


def test_objects_equality():
    """ it should return true if objects are equal """
    obj_a = {
        "test": [1],
        "hello": "world",
    }
    obj_b = {
        "test": [1],
        "hello": "world",
    }
    assert isjsonequal(obj_a, obj_b)
    assert isjsonequal(obj_b, obj_a)


def test_objects_difference():
    """ it should return false if objects are not equal """
    obj_a = {
        "test": [1],
        "hello": "mundo",
        "config": {
            "test": "test",
        }
    }
    obj_b = {
        "test": [1],
        "hello": "world",
        "config": {
            "test": "test",
        }
    }

    assert not isjsonequal(obj_a, obj_b)
    assert not isjsonequal(obj_b, obj_a)


def test_objects_deep_difference():
    """ it should return false if at least one deep property is not equal """
    obj_a = {
        "test": [1],
        "hello": "mundo",
        "config": {
            "test": "test",
        }
    }
    obj_b = {
        "test": [1],
        "hello": "mundo",
        "config": {
            "test": "not_test",
        }
    }
    assert not isjsonequal(obj_a, obj_b)
    assert not isjsonequal(obj_b, obj_a)


def test_partial_objects_difference():
    """ it should detect difference between an object and its subset """
    obj_a = {
        "hello": "mundo",
        "config": {
            "test": "test",
        }
    }
    obj_b = {
        "config": {
            "test": "test",
        }
    }
    assert not isjsonequal(obj_a, obj_b)
    assert not isjsonequal(obj_b, obj_a)
