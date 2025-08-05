import pytest

from pkg.response import HttpCode


class TestAppHandler:
    @pytest.mark.parametrize(
        "app_id, query",
        [("1232ea07-8045-4452-88f9-9c7e7189e673", None), ("1232ea07-8045-4452-88f9-9c7e7189e673", "你好，你是?")],
    )
    def test_completion(self, app_id, query, client):
        resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        print(resp.json)
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
