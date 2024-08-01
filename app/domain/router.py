from fastapi import APIRouter, UploadFile, Form, File, Body,Depends,status,Body
from domain.models import *
from fastapi.responses import StreamingResponse
from domain.docs_fill import draw_text_on_image
from domain.match_item import *
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/ai",
)

def checker(data: str = Form(...)):
    try:
        return DocsFillRequest(**json.loads(data))  # JSON 데이터를 DocsFillRequest 모델로 파싱
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@router.post("/docsfill")
async def docs_fill(image: UploadFile = File(...), data: DocsFillRequest = Depends(checker)) :
    try:
        filled_empty_items = await match(data)
        print(filled_empty_items)
        print("-------------------------------------")
        translate_items = [] #await translate(data)
        print(translate_items)
        image_stream = await image.read()
        img_byte_arr = draw_text_on_image(image_stream, filled_empty_items,translate_items)
        return StreamingResponse(img_byte_arr, media_type="image/jpeg")
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(e.errors())
        )    
