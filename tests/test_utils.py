from kafka_connect_sync.utils import is_json_equal

def test_objects_equality():
  base = {
    "test": [1],
    "hello": "world",
  }
  obj = {
    "test": [1],
    "hello": "world",
  }
  assert is_json_equal(base, obj)
  assert is_json_equal(obj, base)


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

  assert is_json_equal(base, obj) == False
  assert is_json_equal(obj, base) == False


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
  assert is_json_equal(base, obj) == False
  assert is_json_equal(obj, base) == False

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
  assert is_json_equal(base, obj) == False
  assert is_json_equal(obj, base) == False

