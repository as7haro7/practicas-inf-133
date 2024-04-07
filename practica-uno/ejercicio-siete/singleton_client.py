import requests

ep="partidas"
url = f"http://localhost:8000/{ep}"


# - POST `/partidas`
nuevo_elemento = {
  "elemento": "papel"
}
response = requests.request(
    method="POST", url=url, json=nuevo_elemento
)
print(response.text)

# - GET `/partidas`
response = requests.request(method="GET", url=url)
print(response.text)

# - GET `/partidas?resultado={resultado}`
resultado = "empate"
url_get_res = f"{url}?resultado={resultado}"
response = requests.request(method="GET", url=url_get_res)
print(response.text)

