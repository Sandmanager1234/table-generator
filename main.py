import aiofiles
from fastapi import FastAPI, Request, status, HTTPException, File, UploadFile, Form, Depends, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from datetime import date

from models.parsing_models import PriceMaker

app = FastAPI()

templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {
        'request': req
    })


@app.get('/sklad', response_class=HTMLResponse)
async def skald(req: Request):
    return templates.TemplateResponse('sklads.html', {
        'request': req
    })


@app.post('/api/skalds')
async def api_sklads(
        input_file: UploadFile,
        yuan: str = Form(default='100')
):
    async with aiofiles.open(input_file.filename, 'wb') as file:
        await file.write(await input_file.read())

    return JSONResponse({
        'status': 'SUCCSES!',
        'filename': input_file.filename,
        'yuan': float(yuan)
    })


@app.get('/prices')
async def prices(req: Request):
    return templates.TemplateResponse('prices.html', {
        'request': req
    })


@app.post('/api/prices_files')
async def api_prices_files(files: list[UploadFile] | None = None):
    if not os.path.isdir(f'files/{date.today()}'):
        print(f'Create new folder with name {date.today()}')
        os.mkdir(f'files/{date.today()}')
    for file in files:
        async with open(f'files/{date.today()}/{file.filename}', 'wb') as new_file:
            await new_file.write(await file.read())


@app.post('/api/prices')
async def api_prices(
        body: PriceMaker = Depends(PriceMaker.as_form)
):
    return JSONResponse({
        'status': 'SUCCSESS!',
        'table_one_name': table_one.filename,
        'table_two_name': table_two.filename,
        'price_maker': body.yuan
    })
