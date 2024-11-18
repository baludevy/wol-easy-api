import re
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prisma import Prisma
from contextlib import asynccontextmanager

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/add_host")
async def add_host(ip_addr: str, mac_addr: str):
    if validate_ip(ip_addr) and validate_mac(mac_addr):
        data = await db.host.create({"ip_address": ip_addr, "mac_address": mac_addr})
        return data
    return JSONResponse({"message": "invalid input"}, status_code=400)

@app.post("/delete_host")
async def delete_host(host: str):
    await db.host.delete(where={'id': host})
    return "cool"


@app.post("/send_wol")
async def send_wol(host: str):
    try:
        data = await db.host.find_unique_or_raise(where={'id': host})
        wol(data.mac_address)
        return JSONResponse({"message": "cool"})
    except:
        return JSONResponse({"message": "host not found"}, status_code=404)
    

@app.get("/list_hosts")
async def list_hosts():
    data = await db.host.find_many()
    return data



def wol(mac_addr: str) -> None:
    print(f"yeah i absolutely sent the wol request to {mac_addr}")

def validate_ip(ip: str) -> bool:
    regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip):
        return True
    return False


def validate_mac(mac: str) -> bool:
    regex = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    if re.search(regex, mac):
        return True
    return False
