from domain.models import *
from domain.openai_util import *

async def match(request: DocsFillRequest) -> dict[Coordi,ItemInfo] :

    filled_empty_items = {}
    member_info = request.memberInfo
    emptyItems = request.docsInfoDTO.emptyItems
    for item in emptyItems:
        coordi = Coordi(top=item.top, left=item.left, width=item.width, height=item.height)
        
        # GPT API를 호출하여 ItemInfo를 생성
        item_info = await generate_item_info(item, member_info)
        filled_empty_items[coordi] = item_info

    return filled_empty_items

async def translate(request: DocsFillRequest) -> list[Item] :

    translate_items = []
    items = request.docsInfoDTO.items
    for item in items:
        #coordi = Coordi(top=item.top, left=item.left)
        # GPT API를 호출하여 ItemInfo를 생성
        text = await generate_translate_item(item.columnName,request.docsInfoDTO.translate)
        item.columnName = text
        translate_items.append(item)

    return translate_items
