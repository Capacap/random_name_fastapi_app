import namegen as ng
import main
from fastapi.testclient import TestClient

client = TestClient(main.app)

def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "Server is running"}

def test_get_countries():
   response = client.get("/countries")
   assert response.status_code == 200
   countries = ng.get_countries(main.df)
   assert response.json() == {"countries": countries}

def test_get_random_names():
    country = "sweden"
    count = 10
    response = client.get(f"/random_names?country={country}&count={count}")
    assert response.status_code == 200
    assert len(response.json()["random_names"]) == count

def test_get_random_male_names():
    country = "sweden"
    count = 10
    response = client.get(f"/random_male_names?country={country}&count={count}")
    assert response.status_code == 200
    assert len(response.json()["random_male_names"]) == count

def test_get_random_female_names():
    country = "sweden"
    count = 10
    response = client.get(f"/random_female_names?country={country}&count={count}")
    assert response.status_code == 200
    assert len(response.json()["random_female_names"]) == count
