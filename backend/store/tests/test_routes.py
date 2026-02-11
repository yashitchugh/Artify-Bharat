import pytest
import os
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response

load_dotenv()


@pytest.mark.db
class TestSignup:
    def test_signup(self,api_client):
        pass


@pytest.mark.db
class TestLogin:
    def test_login_returns_200(self,api_client):
        pass

@pytest.mark.db
class TestProducts:
    pass


@pytest.mark.db
class TestDashboardStats:
    def test_get_stats_returns_200(self,api_client):
        email = os.getenv('ARTISAN_EMAIL')
        password = os.getenv('ARTISAN_PASS')
        response :Response = api_client.post('api/token/',{
            'email': email,
            'password':  password
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['user_type'] == 'artisan'
        access_token = response.data['access']
        response = api_client.post('store/stats/',access_token)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stats_returns_401(self,api_client):
        email = os.getenv('BUYER_EMAIL')
        password = os.getenv('BUYER_PASS')
        response :Response = api_client.post('api/token/',{
            'email': email,
            'password':  password
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['user_type'] == 'buyer'
        access_token = response.data['access']
        response = api_client.post('store/stats/',access_token)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


        