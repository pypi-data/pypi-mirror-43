import hashlib
import uuid

from flask import Flask
from flask import url_for

import pytest

from taar import ProfileFetcher
from taar import recommenders
from taar.context import default_context
from taar.profile_fetcher import ProfileController

try:
    from unittest.mock import MagicMock
except Exception:
    from mock import MagicMock


def hasher(uuid):
    return hashlib.new("sha256", str(uuid).encode("utf8")).hexdigest()


def create_recommendation_manager():
    root_ctx = default_context()
    pf = ProfileFetcher(root_ctx)
    pf.set_client(ProfileController(root_ctx, "us-west-2", "taar_addon_data_20180206"))
    root_ctx["profile_fetcher"] = pf
    r_factory = recommenders.RecommenderFactory(root_ctx.child())
    root_ctx["recommender_factory"] = r_factory
    rm = recommenders.RecommendationManager(root_ctx.child())
    return rm


@pytest.fixture
def app():
    from taar.plugin import configure_plugin
    from taar.plugin import PROXY_MANAGER

    flask_app = Flask("test")

    # Clobber the default recommendation manager with a MagicMock
    mock_recommender = MagicMock()
    PROXY_MANAGER.setResource(mock_recommender)

    configure_plugin(flask_app)

    return flask_app


def test_empty_results_by_default(client, app):
    # The default behaviour under test should be that the
    # RecommendationManager simply no-ops everything so we get back an
    # empty result list.
    res = client.post("/v1/api/recommendations/not_a_real_hash/")
    assert res.json == {"results": []}


def test_only_promoted_addons_post(client, app):
    # POSTing a JSON blob allows us to specify promoted addons to the
    # TAAR service.
    res = client.post(
        "/v1/api/recommendations/not_a_real_hash/",
        json=dict(
            {"options": {"promoted": [["guid1", 10], ["guid2", 5], ["guid55", 8]]}}
        ),
        follow_redirects=True,
    )
    # The result should order the GUIDs in descending order of weight
    assert res.json == {"results": ["guid1", "guid55", "guid2"]}


class FakeRecommendationManager(object):
    def __init__(self, *args, **kwargs):
        pass


class StaticRecommendationManager(FakeRecommendationManager):

    # Recommenders must return a list of 2-tuple results
    # with (GUID, weight)
    def recommend(self, client_id, limit, extra_data={}):
        result = [
            ("test-addon-1", 1.0),
            ("test-addon-2", 1.0),
            ("test-addon-N", 1.0),
        ]
        return result


class LocaleRecommendationManager(FakeRecommendationManager):
    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get("locale", None) == "en-US":
            return [("addon-Locale", 1.0)]
        return []


class EmptyRecommendationManager(FakeRecommendationManager):
    def recommend(self, client_id, limit, extra_data={}):
        return []


class PlatformRecommendationManager(FakeRecommendationManager):
    def recommend(self, client_id, limit, extra_data={}):
        if extra_data.get("platform", None) == "WOW64":
            return [("addon-WOW64", 1.0)]
        return []


@pytest.fixture
def locale_recommendation_manager(monkeypatch):
    # Force the plugin configuration
    import os

    os.environ["TAAR_API_PLUGIN"] = "taar.plugin"

    import taar.flask_app

    taar.flask_app.APP_WRAPPER.set({"PROXY_RESOURCE": LocaleRecommendationManager()})


@pytest.fixture
def empty_recommendation_manager(monkeypatch):
    # Force the plugin configuration
    import os

    os.environ["TAAR_API_PLUGIN"] = "taar.plugin"

    import taar.flask_app

    taar.flask_app.APP_WRAPPER.set({"PROXY_RESOURCE": EmptyRecommendationManager()})


@pytest.fixture
def platform_recommendation_manager(monkeypatch):
    # Force the plugin configuration
    import os

    os.environ["TAAR_API_PLUGIN"] = "taar.plugin"

    import taar.flask_app

    taar.flask_app.APP_WRAPPER.set({"PROXY_RESOURCE": PlatformRecommendationManager()})


@pytest.fixture
def static_recommendation_manager(monkeypatch):
    # Force the plugin configuration
    import os

    os.environ["TAAR_API_PLUGIN"] = "taar.plugin"

    import taar.flask_app

    taar.flask_app.APP_WRAPPER.set({"PROXY_RESOURCE": StaticRecommendationManager()})


def test_empty_recommendation(client, empty_recommendation_manager):
    response = client.post(
        url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == b'{"results": []}'


def test_locale_recommendation(client, locale_recommendation_manager):
    response = client.post(
        url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
        + "?locale=en-US"
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == b'{"results": ["addon-Locale"]}'

    response = client.post(
        url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == b'{"results": []}'


def test_platform_recommendation(client, platform_recommendation_manager):
    uri = (
        url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
        + "?platform=WOW64"
    )
    response = client.post(uri)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == b'{"results": ["addon-WOW64"]}'

    response = client.post(
        url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == b'{"results": []}'


def test_simple_request(client, static_recommendation_manager):
    url = url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    response = client.post(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    expected = b'{"results": ["test-addon-1", "test-addon-2", "test-addon-N"]}'
    assert response.data == expected


def test_mixed_and_promoted_and_taar_adodns(client, static_recommendation_manager):
    """
    Test that we can provide addon suggestions that also get clobbered
    by the promoted addon set.
    """
    url = url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    res = client.post(
        url,
        json=dict(
            {"options": {"promoted": [["guid1", 10], ["guid2", 5], ["guid55", 8]]}}
        ),
        follow_redirects=True,
    )
    # The result should order the GUIDs in descending order of weight
    expected = {
        "results": [
            "guid1",
            "guid55",
            "guid2",
            "test-addon-1",
            "test-addon-2",
            "test-addon-N",
        ]
    }
    assert res.json == expected


def test_overlapping_mixed_and_promoted_and_taar_adodns(client, static_recommendation_manager):
    """
    Test that we can provide addon suggestions that also get clobbered
    by the promoted addon set.
    """
    url = url_for("recommendations", hashed_client_id=hasher(uuid.uuid4()))
    res = client.post(
        url,
        json=dict(
            {"options": {"promoted": [["test-addon-1", 10], ["guid2", 5], ["guid55", 8]]}}
        ),
        follow_redirects=True,
    )
    # The result should order the GUIDs in descending order of weight
    expected = {
        "results": [
            "test-addon-1",
            "guid55",
            "guid2",
            "test-addon-2",
            "test-addon-N",
        ]
    }
    assert res.json == expected
