from kafkaconnectsync.utils import isjsonequal

def test_objects_equality():
  base = {
    "test": [1],
    "hello": "world",
  }
  obj = {
    "test": [1],
    "hello": "world",
  }
  assert isjsonequal(base, obj)
  assert isjsonequal(obj, base)


def test_objects_difference():
  base = {
    "test": [1],
    "hello": "mundo",
    "config": {
      "test": "test",
    }
  }
  obj = {
    "test": [1],
    "hello": "world",
    "config": {
      "test": "test",
    }
  }

  assert isjsonequal(base, obj) == False
  assert isjsonequal(obj, base) == False


def test_objects_deep_difference():
  base = {
    "test": [1],
    "hello": "mundo",
    "config": {
      "test": "test",
    }
  }
  obj = {
    "test": [1],
    "hello": "mundo",
    "config": {
      "test": "not_test",
    }
  }
  assert isjsonequal(base, obj) == False
  assert isjsonequal(obj, base) == False

def test_partial_objects_difference():
  base = {
    "hello": "mundo",
    "config": {
      "test": "test",
    }
  }
  obj = {
    "config": {
      "test": "test",
    }
  }
  assert isjsonequal(base, obj) == False
  assert isjsonequal(obj, base) == False

