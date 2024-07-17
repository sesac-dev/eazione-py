from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from domain.models import ItemInfo,Coordi

def draw_text_on_image(image_stream, data:dict[Coordi, ItemInfo]):
    # 이미지 열기
    image = Image.open(BytesIO(image_stream))
    
    # 이미지를 RGBA에서 RGB로 변환합니다
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    draw = ImageDraw.Draw(image)

    # 폰트 설정 (여기서는 기본 폰트를 사용합니다. 다른 폰트를 사용하려면 경로를 지정하세요.)
    try:
        font = ImageFont.truetype("arial.ttf", 15)  # 시스템에 Arial 폰트가 설치되어 있어야 합니다.
    except IOError:
        font = ImageFont.load_default()

    # # 딕셔너리를 돌면서 이미지 위에 텍스트 그리기
    # for key, value in data.items():
    #     if value:  # 값이 비어있지 않은 경우에만 그리기
    #         top, left = map(float, key.strip("()").split(","))
    #         draw.text((left, top), value, fill="Blue", font=font)

    # 데이터 딕셔너리를 돌면서 이미지 위에 텍스트 그리기
    for coordi, item_info in data.items():
        text = item_info.text
        if item_info.is_check:
            text="V"
        if text:  # 텍스트가 비어있지 않은 경우에만 그리기
            top = coordi.top+5
            left = coordi.left+10
            fill_color = (80, 80, 80) if item_info.is_ex else "Blue"
            draw.text((left, top), text, fill=fill_color, font=font)

    # 이미지를 바이트 배열로 저장합니다
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr