from src.app import app
import re


def test_root_get():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert re.search(r'Upload a picture', str(response.data)) is not None


def test_root_post_serves_predictions():
    image = open("/app/ml_model_app/samples/4_sample_1.png", "rb")
    data = dict(
        file=(image, 'file'),
    )
    response = app.test_client() \
        .post('/', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert re.search(r'Prediction: 4', str(response.data)) is not None
