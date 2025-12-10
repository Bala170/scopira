import requests

API = "http://localhost:5000/api"

checks = [
    ("root", "http://localhost:5000/", "GET", None),
    ("auth_register_schema", f"{API}/auth/register", "POST", {
        "username": "health.check@example.com",
        "email": "health.check@example.com",
        "password": "Test123!",
        "first_name": "Health",
        "last_name": "Check",
        "profession": "Tester"
    }),
    ("auth_login", f"{API}/auth/login", "POST", {
        "email": "health.check@example.com",
        "password": "Test123!"
    })
]

for name, url, method, body in checks:
    try:
        if method == "GET":
            r = requests.get(url, timeout=5)
        else:
            r = requests.post(url, json=body, timeout=8)
        print(f"{name}: {r.status_code} -> {r.text[:200]}")
    except Exception as e:
        print(f"{name}: ERROR -> {e}")
