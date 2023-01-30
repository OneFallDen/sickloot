from fastapi import FastAPI
from routers import user_router, balance_router, case_router, inventory_router


app = FastAPI()


app.include_router(user_router.router)
app.include_router(balance_router.router)
app.include_router(case_router.router)
app.include_router(inventory_router.router)
