import shutil
import time
import uvicorn
import aiofiles
from fastapi import FastAPI, Request, status, HTTPException, File, UploadFile, Form, Depends, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from datetime import date

from gens import price_generator, shop_generator, storage_generator

# from models.parsing_models import PriceMaker

app = FastAPI()

templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/', response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {
        'request': req
    })

@app.get("/download/")
async def download_file():
    name = os.listdir('output/out')[0]
    file_path = '//'.join(['output/out', name])
    return FileResponse(path=file_path, filename=name)


@app.get('/sklad', response_class=HTMLResponse)
async def skald(req: Request):
    return templates.TemplateResponse('sklads.html', {
        'request': req
    })


@app.get('/prices')
async def prices(req: Request):
    return templates.TemplateResponse('prices.html', {
        'request': req
    })


@app.get('/excel')
async def excel(req: Request):
    return templates.TemplateResponse('excel.html', {
        'request': req
    })

@app.get('/success')
async def succes_page(req: Request):
    return templates.TemplateResponse(
        'success.html', 
        {'request': req}
        )

@app.post('/price-api')
async def get_params(input_file: UploadFile = Form(...), yuan: str = Form(...)):
    if not input_file:
        return RedirectResponse(url='/page1', headers={"Location": "/success"}, status_code=302)
    else:
        file_path = os.path.join("input\\table1", input_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(input_file.file, buffer)
        try:
            # out = price_generator.create_first_table(float(yuan))
            # Не работает, там поменяли название страницы
            # print(out)
            time.sleep(30)
            pass
        except Exception as ex:
            print(ex)
        return RedirectResponse(url="/success", headers={"Location": "/success"}, status_code=302)
    

@app.post('/sklads-api/')
async def get_params(input_file: UploadFile = Form(...)):
    if not input_file:
        return RedirectResponse(url='/page1', headers={"Location": "/success"}, status_code=302)
    else:
        file_path = os.path.join("input\\table2\\", input_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(input_file.file, buffer)
        try:
            storage_generator.create_storages()
        except Exception as ex:
            print(ex)
        return RedirectResponse(url="/success", headers={"Location": "/success"}, status_code=302)

@app.post('/excel-api/')
async def gen_files():
    return {'Status': 'SUPER'}


# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)
