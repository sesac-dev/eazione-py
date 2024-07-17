import openai
from domain.models import *

openai.api_key = 'YOUR_API_KEY'

async def generate_item_info(column_name: str, member_info: MemberInfo) -> ItemInfo:
    # OpenAI API를 호출하기 위한 프롬프트 작성
    prompt = f"""
    Given the following member information:
    Passport Info:
    - Passport Number: {member_info.passportInfo.passportNumber}
    - Sure Name: {member_info.passportInfo.sureName}
    - Given Names: {member_info.passportInfo.givenNames}
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
    - Number: {member_info.identityCardInfo.number}
    - Name: {member_info.identityCardInfo.name}
    - County: {member_info.identityCardInfo.county}
    - Status: {member_info.identityCardInfo.status}
    - Issue Date: {member_info.identityCardInfo.issueDate}
    - Start Date of Stay: {member_info.identityCardInfo.startDateOfStay}
    - End Date of Stay: {member_info.identityCardInfo.endDateOfStay}
    - Address: {member_info.identityCardInfo.address}
    - Report Date: {member_info.identityCardInfo.reportDate}

    General Info:
    - Email: {member_info.email}
    - Name: {member_info.name}
    - Income: {member_info.income}
    - Housing Type: {member_info.housingType}

    Based on this information, please match the column name "{column_name}" to the most relevant piece of information. If an exact match cannot be found, please generate a fictional piece of data and set is_ex to True.

    Provide the result in the following JSON format:
    {{
        "is_check": Fasle,
        "is_ex": True or False,
        "text": "matched or fictional data"
    }}
    """
    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # 응답 데이터 파싱
    item_info_data = response['choices'][0]['message']['content']
    item_info = ItemInfo.parse_raw(item_info_data)

    return item_info



#     # 데이터를 GPT API에 전달할 프롬프트 형식으로 준비
#     prompt = f"""
#     You are given a column name and member information. Your task is to find the semantically matching information from the member data for the given column name. If no matching information is found, generate a dummy text based on the column name and set 'is_ex' to true. Otherwise, set 'is_ex' to false.
#     Column Name: {column_name}
#     Member Info:
#     Return a dictionary with keys 'is_check', 'is_ex', and 'text'.
#     """

#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )

#     response_text = response.choices[0].text.strip()
#     gpt_response = eval(response_text)
    
#     item_info = ItemInfo(
#         is_check=gpt_response['is_check'],
#         is_ex=gpt_response['is_ex'],
#         text=gpt_response['text']
#     )
    
#     return item_info
