from flask import url_for
from app import app as flask_app
from app import cache
from app.controllers import create_md5
import pytest

@pytest.fixture
def app():
    return flask_app

def test_ping(client):
    assert client.get(url_for("ping")).status_code == 200

# Erros
def test_posts_tags_requirement(client):
    url = url_for("posts", tags='')
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Tags parameter is required"}

def test_posts_sortby_invalid(client):
    url = url_for("posts", tags='science,tech', sortBy='notexist')
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_json() == {"error": "sortBy parameter is invalid"}

# Success
def test_posts_success_one_tag(client):
    url = url_for("posts", tags='tech')
    response = client.get(url)
    assert response.status_code == 200
    json = response.get_json()["posts"]
    assert len(json) == 28
    assert json[0]["id"] == 1

def test_posts_success_two_tags(client):
    url = url_for("posts", tags='tech,science')
    response = client.get(url)
    assert response.status_code == 200
    json = response.get_json()["posts"]
    assert len(json) == 49
    assert json[0]["id"] == 1


def test_posts_success_sortBy_id(client):
    url = url_for("posts", tags='tech', sortBy='id')
    response = client.get(url)
    assert response.status_code == 200
    json = response.get_json()["posts"]
    assert json[0]["id"] == 1
    assert json[-1]["id"] == 99

def test_posts_success_sortBy_likes(client):
    url = url_for("posts", tags='tech', sortBy='likes')
    response = client.get(url)
    assert response.status_code == 200
    json = response.get_json()["posts"]
    assert json[0]["likes"] == 25
    assert json[-1]["likes"] == 985

def test_posts_success_direction_desc(client):
    url = url_for("posts", tags='tech', sortBy='id', direction='desc')
    response = client.get(url)
    assert response.status_code == 200
    json = response.get_json()["posts"]
    assert json[-1]["id"] == 1
    assert json[0]["id"] == 99

def test_posts_success_cache(client):
    url = url_for("posts", tags='tech', sortBy='id', direction='desc')
    response = client.get(url)
    md5 = create_md5('tech', 'id', 'desc')
    assert response.status_code == 200
    json = response.get_json()
    assert json == cache.get(md5)

