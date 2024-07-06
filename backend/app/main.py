from fastapi import FastAPI

models.Base.metadata.create_all(bind=engine)

app = FastAPI()