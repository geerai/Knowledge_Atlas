import importlib
import sys

from fastapi.testclient import TestClient


def _load_auth_server(monkeypatch, tmp_path):
    monkeypatch.setenv("KA_DB_PATH", str(tmp_path / "ka_auth.db"))
    monkeypatch.setenv("KA_SECRET_FILE", str(tmp_path / "ka_auth_secret.txt"))
    monkeypatch.setenv("KA_PUBLIC_SITE_URL", "http://testserver")
    sys.modules.pop("ka_auth_server", None)
    import ka_auth_server  # type: ignore
    return importlib.reload(ka_auth_server)


def test_github_username_round_trip(monkeypatch, tmp_path):
    mod = _load_auth_server(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.pwd_context, "hash", lambda secret: "hashed$" + secret)
    monkeypatch.setattr(mod.pwd_context, "verify", lambda secret, hashed: hashed == ("hashed$" + secret))

    with TestClient(mod.app) as client:
        reg = client.post("/auth/register", json={
            "email": "student@ucsd.edu",
            "password": "atlaspass123",
            "first_name": "Test",
            "last_name": "Student",
            "department": "COGS",
            "track": "",
            "question_id": "",
        })
        assert reg.status_code == 201

        login = client.post("/auth/login", json={
            "email": "student@ucsd.edu",
            "password": "atlaspass123",
        })
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        save = client.post("/auth/github-username", headers=headers, json={
            "github_username": "https://github.com/Test-Student",
            "source": "explicit",
        })
        assert save.status_code == 200
        body = save.json()
        assert body["github_username"] == "test-student"
        assert body["github_username_source"] == "explicit"
        assert body["github_username_updated_at"]

        me = client.get("/auth/me", headers=headers)
        assert me.status_code == 200
        user = me.json()
        assert user["github_username"] == "test-student"
        assert user["github_username_source"] == "explicit"
        assert user["github_username_updated_at"]
