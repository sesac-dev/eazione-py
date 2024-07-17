from domain.models import *
from domain.openai_util import generate_item_info

async def match(request: DocsFillRequest):
    # data = {
    #     "(225.51976, 102.49523)": "",
    #     "(281.0, 110.0)": "",
    #     "(318.0, 112.0)": "",
    #     "(355.09015, 101.684875)": "",
    #     "(352.0, 291.0)": "",
    #     "(410.27762, 100.08113)": "",
    #     "(410.0, 332.0)": "",
    #     "(225.44818, 354.37732)": "",
    #     "(225.0, 624.0)": "",
    #     "(279.03836, 355.97192)": "",
    #     "(318.2317, 355.16876)": "",
    #     "(353.425, 356.76498)": "",
    #     "(411.0, 365.0)": "",
    #     "(244.0, 694.0)": "",
    #     "(485.43527, 207.22072)": "Tanaka",
    #     "(486.18277, 435.92133)": "Yuki Tanaka",
    #     "(526.2202, 235.20386)": "1985",
    #     "(526.19116, 367.14526)": "05",
    #     "(526.1774, 429.52017)": "15",
    #     "(512.0, 580.0)": "F",
    #     "(506.10544, 765.4154)": "Japan",
    #     "(553.39966, 303.97)": "Z12345678",
    #     "(583.0148, 203.21432)": "J12345678",
    #     "(587.7539, 491.89105)": "2019-05-01",
    #     "(582.09796, 764.6081)": "2029-05-01",
    #     "(619.0071, 201.61201)": "Seoul, South Korea",
    #     "(671.7775, 295.16354)": "Tokyo",
    #     "(669.28735, 772.59753)": "",
    #     "(708.51807, 580.64905)": "",
    #     "(747.0, 595.0)": "",
    #     "(745.2733, 806.9819)": "",
    #     "(774.94995, 331.13855)": "",
    #     "(807.7433, 331.13565)": "",
    #     "(774.1107, 566.24774)": "",
    #     "(807.70557, 566.2445)": "",
    #     "(774.8762, 771.7874)": "",
    #     "(807.6726, 771.7842)": "",
    #     "(841.33636, 331.1327)": "75000000",
    #     "(843.66876, 770.9809)": "",
    #     "(863.7318, 330.33105)": "",
    #     "(866.0963, 567.0388)": "yuki.tanaka@example.com",
    #     "(885.29333, 567.03705)": "",
    #     "(921.31964, 331.9253)": ""
    # }
#     data = [
#     {
#         "Coordi": {
#             "top": 225.51976,
#             "left": 102.49523
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "외국인 등록 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 281.0,
#             "left": 110.0
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "등록증 재발급 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 318.0,
#             "left": 112.0
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "체류기간 연장허가 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 355.09015,
#             "left": 101.684875
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "체류자격 변경 허가 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 352.0,
#             "left": 291.0
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "E-2"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 410.27762,
#             "left": 100.08113
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "체류 자격 부여 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 410.0,
#             "left": 332.0
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "Dummy 체류자격 부여 희망 자격"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 225.44818,
#             "left": 354.37732
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "체류 자격 외 활동 허가 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 225.0,
#             "left": 624.0
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "Dummy 체류 자격 외 활동허가 희망 자격"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 279.03836,
#             "left": 355.97192
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "근무처 변경 및 추가허가 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 318.2317,
#             "left": 355.16876
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "재입국 허가 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 353.425,
#             "left": 356.76498
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "체류지 변경신고 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 411.0,
#             "left": 365.0
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "등록사항 변경신고 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 244.0,
#             "left": 694.0
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "프로필 사진"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 485.43527,
#             "left": 207.22072
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "Tanaka"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 486.18277,
#             "left": 435.92133
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "Yuki"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 526.2202,
#             "left": 235.20386
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "1985"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 526.19116,
#             "left": 367.14526
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "05"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 526.1774,
#             "left": 429.52017
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "15"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 512.0,
#             "left": 580.0
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "F"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 506.10544,
#             "left": 765.4154
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "Japan"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 553.39966,
#             "left": 303.97
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "010-0000-0000"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 583.0148,
#             "left": 203.21432
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "J12345678"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 587.7539,
#             "left": 491.89105
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "2019-05-01"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 582.09796,
#             "left": 764.6081
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "2029-05-01"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 619.0071,
#             "left": 201.61201
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "Seoul, South Korea"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 671.7775,
#             "left": 295.16354
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "123-4567 Tokyo, Japan"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 669.28735,
#             "left": 772.59753
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "010-0000-0000"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 708.51807,
#             "left": 580.64905
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "ABC University"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 747.0,
#             "left": 595.0
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "인가 학교 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 745.2733,
#             "left": 806.9819
#         },
#         "ItemInfo": {
#             "is_check": True,
#             "is_ex": False,
#             "text": "비인가 학교 확인"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 774.94995,
#             "left": 331.13855
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "XYZ Corp"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 807.7433,
#             "left": 331.13565
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "XYZ Corp"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 774.1107,
#             "left": 566.24774
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "123-45-67890"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 807.70557,
#             "left": 566.2445
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "123-45-67890"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 774.8762,
#             "left": 771.7874
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "02-123-4567"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 807.6726,
#             "left": 771.7842
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "02-123-4567"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 841.33636,
#             "left": 331.1327
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "75000000"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 843.66876,
#             "left": 770.9809
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "Software Developer"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 863.7318,
#             "left": 330.33105
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "6 months"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 866.0963,
#             "left": 567.0388
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": False,
#             "text": "yuki.tanaka@example.com"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 885.29333,
#             "left": 567.03705
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "123-456-7890"
#         }
#     },
#     {
#         "Coordi": {
#             "top": 921.31964,
#             "left": 331.9253
#         },
#         "ItemInfo": {
#             "is_check": False,
#             "is_ex": True,
#             "text": "2024-01-01"
#         }
#     }
# ]
    filled_items = {}

    member_info = request.memberInfo
    items = request.docsInfoDTO.items
    for item in items:
        coordi = Coordi(top=item.top, left=item.left)
        column_name = item.columnName
        
        # GPT API를 호출하여 ItemInfo를 생성
        item_info = await generate_item_info(column_name, member_info)
        filled_items[coordi] = item_info


    # #더미데이터 테스트용
    # for entry in data:
    #     coordi = Coordi(**entry["Coordi"])
    #     item_info = ItemInfo(**entry["ItemInfo"])
    #     filled_items[coordi] = item_info
    

    return filled_items
