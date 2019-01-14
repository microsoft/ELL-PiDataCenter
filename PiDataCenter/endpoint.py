import os

url = os.getenv("RPI_CLUSTER")
if not url:
    raise Exception("Missing environment variable: RPI_CLUSTER")

apikey = os.getenv("RPI_APIKEY")
if not apikey:
    raise Exception("Missing environment variable: RPI_APIKEY")

password = os.getenv("RPI_PASSWORD")
if not password:
    raise Exception("Missing environment variable: RPI_PASSWORD")
