from openai import OpenAI
from domain.models import *
import json
import config
from datetime import datetime

client = OpenAI(api_key=config.OPENAI_KEY)

async def generate_item_info(item: Item, member_info: MemberInfo) -> ItemInfo:
    today = datetime.today().strftime("%Y-%m-%d")
    # OpenAI API를 호출하기 위한 프롬프트 작성
    prompt = f"""
    Given the following member information:
    Passport Info:
    - Passport Number: {member_info.passportInfo.passportNumber}
    - Sur Name: {member_info.passportInfo.surName}
    - Given Name: {member_info.passportInfo.givenName}
    - Date of Birth: {member_info.passportInfo.dateOfBirth}
    - Sex: {member_info.passportInfo.sex}
    - Nationality: {member_info.passportInfo.nationality}
    - Date of Issue: {member_info.passportInfo.dateOfIssue}
    - Expiry Date: {member_info.passportInfo.expiryOfDate}
    - Issuing Authority: {member_info.passportInfo.issuingAuthority}
    - Place of Birth: {member_info.passportInfo.placeOfBirth}
    - Type: {member_info.passportInfo.type}
    - Country of Issue: {member_info.passportInfo.countryOfIssue}

    Identity Card Info:
    - ForeignNumber: {member_info.identityCardInfo.foreignNumber}
    - Name: {member_info.identityCardInfo.name}
    - Country: {member_info.identityCardInfo.country}
    - Status: {member_info.identityCardInfo.status}
    - Issue Date: {member_info.identityCardInfo.issueDate}
    - Start Date of Stay: {member_info.identityCardInfo.startDateOfStay}
    - End Date of Stay: {member_info.identityCardInfo.endDateOfStay}
    - Address: {member_info.identityCardInfo.address}
    - Report Date: {member_info.identityCardInfo.reportDate}

    General Info:
    - Email: {member_info.email}
    - Name: {member_info.name}
    - ProfileImage: {member_info.profileImage}
    - Income: {member_info.income}
    - Housing Type: {member_info.housingType}


    Based on this information, please match the column name "{item.columnName}" to the most relevant piece of information and enter the data into 'text'. You must follow these few rules:
    1. If '_idx:num' is appended to the column name, only the numth index of the matched data is entered. ex) if the column name is '외국인 등록번호_idx:0' and matched data is 'Z123456781234', enter 'z'.
    2. If the column name is '신청일', enter {today}.
    3. 'yy' means year, 'mm' means month, 'dd' means day. ex) if the column name is 'birthday_dd' and matched data is '19970611', enter '11'.
    4. If an exact match cannot be found, please generate a fictional piece of data.
    5. If {item.check} is true, data is empty string.

    6. Provide the result in the following JSON format:
    {{
        "is_check": {item.check},
        "is_ex": {"true" if item.columnName not in member_info else "false"},
        "text": "matched or fictional data"
    }}

    7. Ensure that the "is_ex" field is set to true only if the data in the "text" field is fictional. If the data is from member_info, set "is_ex" to false.
    8. Only provide the data in the "text" field without any additional labels or prefixes. its type is str.
    """
    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # 응답 데이터 파싱
    response_message = response.choices[0].message.content.strip()
    
    # 불필요한 마크다운 구문 제거
    if response_message.startswith("```json"):
        response_message = response_message[7:]  # ```json 제거
    if response_message.endswith("```"):
        response_message = response_message[:-3]  # ``` 제거
    response_message = response_message.strip()

    # JSON 파싱이 제대로 되는지 확인
    try:
        response_message = response_message.replace('False', 'false').replace('True', 'true')
        item_info_data = json.loads(response_message)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print("------------------------")
        print(response_message)
        print("------------------------")
        item_info_data = json.loads("{\"is_ex\":true,\"is_check\":false,\"text\":\"fail\"}")

    # item_info_data가 딕셔너리인지 확인
    # if not isinstance(item_info_data, dict):
    #     raise ValueError("The response is not a valid JSON object")

    print("-----------------------------")
    print(item_info_data)
    print("-----------------------------")
    # ItemInfo 객체로 변환
    item_info = ItemInfo(**item_info_data)

    return item_info

async def generate_translate_item(text: str, translate: str) -> str:
    # OpenAI API를 호출하기 위한 프롬프트 작성
    prompt = f"""
    Translate the following text to {translate} :
    
    Text: "{text}"

    provide only the translated text without any explanations.
    """

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # 번역된 텍스트 추출
    translated_text = response.choices[0].message.content.strip()
    
    return translated_text
