from src.keras_inference import predict


def test_hello():
    assert predict() == 'hello world'
