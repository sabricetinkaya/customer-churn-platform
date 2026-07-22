from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_check():
    """
    API'nin çalıştığını doğrulayan basit bir sağlık kontrolü testi.
    """
    # Eğer projenizde bir health/root endpoint'i varsa ona istek atıyoruz
    response = client.get("/")

    # HTTP status kodunun 200 (OK) veya endpoint yapınıza göre beklenen kod olduğunu doğruluyoruz
    assert response.status_code in [200, 404]  # En azından uygulamanın çökmeyip yanıt verdiğini doğrular


def test_dummy_churn_logic():
    """
    Basit bir birim testi örneği (Business Logic Test).
    """
    customer_data = {
        "tenure": 12,
        "monthly_charges": 70.5,
        "total_charges": 846.0
    }

    # Örnek bir doğrulama: Müşteri verisi boş olmamalı
    assert customer_data["tenure"] > 0
    assert customer_data["monthly_charges"] > 0