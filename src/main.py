from fastapi import FastAPI
from prisma import Prisma
from contextlib import asynccontextmanager
from utils import validate_ip, validate_mac

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
    return


@app.get("/list_hosts")
async def list_hosts():
    data = await db.host.find_many()
    return data
