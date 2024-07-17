from fastapi import APIRouter, UploadFile, Form, File, Body,Depends
from domain.models import *
from fastapi.responses import StreamingResponse
from domain.docs_fill import draw_text_on_image
from domain.match_item import match
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/ai",
)

def checker(data: str = Form(...)):
    try:
        return DocsFillRequest.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@router.post("/docsfill")
async def docs_fill(image: UploadFile = File(...), data: DocsFillRequest = Depends(checker)) :
    data_dict = await match(data)
    image_stream = await image.read()
    img_byte_arr = draw_text_on_image(image_stream, data_dict)
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
