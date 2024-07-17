from fastapi import APIRouter, UploadFile, Form, File, Body,Depends
from domain.request_models import *
from fastapi.responses import StreamingResponse
from domain.docs_fill import draw_text_on_image
from domain.match_item import match


router = APIRouter(
    prefix="/ai",
)

@router.post("/docsfill")
async def docs_fill(image: UploadFile = File(...)) :
    data_dict = match()
    image_stream = await image.read()
    img_byte_arr = draw_text_on_image(image_stream, data_dict)
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
