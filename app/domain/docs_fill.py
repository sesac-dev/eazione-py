from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from domain.models import *
from collections import Counter
import requests

def draw_text_on_image(image_stream, filled_empty_items:dict[Coordi, ItemInfo], translate_items:list[Item]):
    # 이미지 열기
    image = Image.open(BytesIO(image_stream))
    
    # 이미지를 RGBA에서 RGB로 변환합니다
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    draw = ImageDraw.Draw(image)

    background_color = get_background_color(image)

    # 폰트 설정 (여기서는 기본 폰트를 사용합니다. 다른 폰트를 사용하려면 경로를 지정하세요.)
    try:
        font = ImageFont.truetype("arial.ttf", 13)  # 시스템에 Arial 폰트가 설치되어 있어야 합니다.
    except IOError:
        font = ImageFont.load_default()

    # #번역된 내용 붙이기
    # for item in translate_items:
    #     top = item.top
    #     left = item.left
    #     right = left + item.width
    #     bottom = top + item.height
    #     region = [(left, top), (right, bottom)]
    #     draw.rectangle(region, fill=background_color)
    #     draw.text((left, top), item.columnName, fill="Black", font=font)

    # 데이터 딕셔너리를 돌면서 이미지 위에 텍스트 그리기
    for coordi, item_info in filled_empty_items.items():
        text = item_info.text
        if item_info.is_photo:
            photo_response = requests.get(text)
            overlay_image = Image.open(BytesIO(photo_response.content)).convert('RGBA')
            overlay_image = overlay_image.resize((int(coordi.width), int(coordi.height)))

            # 투명도를 지원하기 위해 알파 채널을 분리하고 새로운 배경에 합성
            r, g, b, a = overlay_image.split()
            overlay_image_rgb = Image.merge('RGB', (r, g, b))
            mask = Image.merge('L', (a,))

            # 오버레이 이미지를 배경 이미지 위에 붙입니다
            image.paste(overlay_image_rgb, (int(coordi.left), int(coordi.top)), mask)
            continue
        if item_info.is_check:
            if item_info.is_ex: continue
            text="V"
        if text:  # 텍스트가 비어있지 않은 경우에만 그리기
            top = coordi.top+5
            left = coordi.left+10
            fill_color = "Red" if item_info.is_ex else "Blue"
            draw.text((left, top), text, fill=fill_color, font=font)

    # 이미지를 바이트 배열로 저장합니다
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr


def get_background_color(image_path):
    # 가장자리 픽셀 추출
    width, height = image_path.size
    pixels = []

    # 상단 및 하단 가장자리 픽셀 추가
    for x in range(width):
        pixels.append(image_path.getpixel((x, 0)))
        pixels.append(image_path.getpixel((x, height - 1)))

    # 왼쪽 및 오른쪽 가장자리 픽셀 추가
    for y in range(height):
        pixels.append(image_path.getpixel((0, y)))
        pixels.append(image_path.getpixel((width - 1, y)))

    # 가장 많이 등장한 색상 찾기
    most_common_color = Counter(pixels).most_common(1)[0][0]

    return most_common_color