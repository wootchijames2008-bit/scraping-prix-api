

def test_lister_livre(client):
    response = client.get("/livres/")
    assert response.status_code == 200

def test_creer_livre(client):
    nouveau_livre = {
        "title": "Fruits Basket, Vol. 2 (Fruits Basket #2)",
        "price": 10.99,
        "rating": 5,
        "stock": True
    }
    response = client.post("/livres/", json=nouveau_livre)
    assert response.status_code == 201
    livre = response.json()
    assert livre["title"] == nouveau_livre["title"]
    assert livre["price"] == nouveau_livre["price"]
    assert livre["rating"] == nouveau_livre["rating"]
    assert livre["stock"] == nouveau_livre["stock"]
    livre_id = livre["id"]
    response_patch = client.patch(f"/livres/{livre_id}", json={"price": 20.20})
    assert response_patch.status_code == 200
    assert response_patch.json()["price"] == 20.20

def test_supprimer_livre(client):
    nouveau_livre = {
        "title": "hhuhuhuhuhuhiu",
        "price": 15.99,
        "rating": 4,
        "stock": True
    }
    response = client.post("/livres/", json=nouveau_livre)
    assert response.status_code == 201
    livre_id = response.json()["id"]
    response_delete = client.delete(f"/livres/{livre_id}")
    assert response_delete.status_code == 200

def test_modifier_livre_inexistant(client):
    response = client.patch("/livres/999", json={"price": 20.20})
    assert response.status_code == 404

def test_supprimer_livre_inexistant(client):
    response = client.delete("/livres/99999")
    assert response.status_code == 404

def test_creer_livre_invalide(client):
    livre_invalide = {
        "title": "test new"
    }
    response = client.post("/livres/", json=livre_invalide)
    assert response.status_code == 422

def test_creer_livre_prix_invalide(client):
    livre_invalide = {
        "title": "Livre prix invalide",
        "price": -10,
        "rating": 5,
        "stock": True
    }

    response = client.post("/livres/", json=livre_invalide)

    assert response.status_code == 422

def test_creer_livre_rating_invalide(client):
    livre_invalide = {
        "title": "Livre rating invalide",
        "price": 15.0,
        "rating": 6,
        "stock": True
    }

    response = client.post("/livres/", json=livre_invalide)

    assert response.status_code == 422

def test_filtre_min_rating(client):
    response = client.get("/livres/?min_rating=5")

    assert response.status_code == 200

    livres = response.json()

    for livre in livres:
        assert livre["rating"] >= 5

def test_filtre_en_stock(client):
    response = client.get("/livres/?en_stock=true")

    assert response.status_code == 200

    livres = response.json()

    for livre in livres:
        assert livre["stock"] is True

def test_tri_prix_asc(client):
    response = client.get("/livres/?tri_prix=asc")

    assert response.status_code == 200

    livres = response.json()
    prix = [livre["price"] for livre in livres]

    assert prix == sorted(prix)

def test_tri_prix_desc(client):
    response = client.get("/livres/?tri_prix=desc")

    assert response.status_code == 200

    livres = response.json()
    prix = [livre["price"] for livre in livres]

    assert prix == sorted(prix, reverse=True)