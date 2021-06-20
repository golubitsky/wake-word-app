from src.app import app


def test_root_get():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, brave world!'


def test_root_post():
    image = open("/app/ml_model_app/samples/4_sample_1.png", "rb")
    data = dict(
        file=(image, 'file'),
    )
    response = app.test_client() \
        .post('/', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.data == b'4'
