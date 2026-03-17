# import time
# import logging 
# from fastapi import FastAPI
# from fastapi.requests import Request
# logger = logging.getLogger("uvicorn.access")
# logging.disable = True

# def register_middleware(app:FastAPI):
    
#     @app.middleware("http")
#     async def custom_logging(request:Request,call_next):

#         start_time = time.time()
#         response = await call_next(request)
#         processing_time = time.time()- start_time
#         message = f"{request.client.host}:{request.client.port}-{request.method} {response.status_code} {processing_time}"