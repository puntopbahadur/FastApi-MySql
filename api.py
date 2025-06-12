#1. GET Request
from playwright.sync_api import sync_playwright
def test_get_request():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get("http://127.0.0.1:8000/items/")

        assert response.status == 200
        json_data = response.json()
        print(json_data)

test_get_request()

#2. Sending POST Request
from playwright.sync_api import sync_playwright
def test_post_request():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.post("http://127.0.0.1:8000/items/",
                                        data={"name": "Reliance", "price": "75000", "is_offer":True})

        assert response.status == 201  # HTTP 201 Created
        print(response.json())

test_post_request()


#3. Sending PUT Request (Update Data)
from playwright.sync_api import sync_playwright
def test_put_request():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.put("http://127.0.0.1:8000/items/8446",
                                       data={"id": 8446, "name": "Reliance Mart", "price": "76000", "is_offer":False})

        assert response.status == 200  # HTTP 200 OK
        print(response.json())

test_put_request()


# 4. Sending DELETE Request
from playwright.sync_api import sync_playwright
def test_delete_request():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.delete("http://127.0.0.1:8000/items/8446")

        assert response.status == 200  # HTTP 200 OK
        print(response.text())  # No content expected

test_delete_request()


#5. Validating Response Time
import time
from playwright.sync_api import sync_playwright

def test_response_time():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        start_time = time.time()
        response = request_context.get("http://127.0.0.1:8000/items")
        end_time = time.time()

        assert response.status == 200
        assert (end_time - start_time) < 1  # Ensure response is under 1 second
        print(f"Response time: {end_time - start_time:.2f} seconds")

test_response_time()

