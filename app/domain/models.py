from typing import List
from pydantic import BaseModel, Field

class PassportInfo(BaseModel):
    passportNumber: str
    sureName: str
    givenNames: str
    dateOfBirth: str
    sex: str
    nationality: str
    dateOfIssue: str
    expiryOfDate: str
    issuingAuthority: str
    placeOfBirth: str
    type: str
    countryOfIssue: str

class IdentityCardInfo(BaseModel):
    number: str
    name: str
    county: str
    status: str
    issueDate: str
    startDateOfStay: str
    endDateOfStay: str
    address: str
    reportDate: str

class MemberInfo(BaseModel):
    email: str
    name: str
    passportInfo: PassportInfo
    identityCardInfo: IdentityCardInfo
    income: int
    housingType: str

class Item(BaseModel):
    columnName: str
    top: float
    left: float
    width: float
    height: float

class DocsInfoDTO(BaseModel):
    title: str
    image: str
    items: List[Item]

class DocsFillRequest(BaseModel):
    memberInfo: MemberInfo
    docsInfoDTO: DocsInfoDTO

class Coordi(BaseModel):
    top: float
    left: float

    def __hash__(self):
        return hash((self.top, self.left))

    def __eq__(self, other):
        if isinstance(other, Coordi):
            return self.top == other.top and self.left == other.left
        return False

class ItemInfo(BaseModel):
    is_check: bool
    is_ex: bool
    text: str

