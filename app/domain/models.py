from typing import List
from pydantic import BaseModel, Field

class PassportInfo(BaseModel):
    passportNumber: str
    surName: str
    givenName: str
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
    foreignNumber: str
    name: str
    country: str
    status: str
    issueDate: str
    startDateOfStay: str
    endDateOfStay: str
    address: str
    reportDate: str

class MemberInfo(BaseModel):
    email: str
    name: str
    profileImage: str
    passportInfo: PassportInfo
    identityCardInfo: IdentityCardInfo
    income: int
    housingType: str
    phoneNumber: str
    currentWorkplace: str
    currentWorkplaceRegistrationNumber: str
    workplacePhoneNumber: str
    signature: str


class Item(BaseModel):
    columnName: str
    top: float
    left: float
    width: float
    height: float
    check: bool
    photo: bool

class DocsInfoDTO(BaseModel):
    title: str
    translate: str
    items: List[Item]
    emptyItems: List[Item]

class DocsFillRequest(BaseModel):
    memberInfo: MemberInfo
    docsInfoDTO: DocsInfoDTO

class Coordi(BaseModel):
    top: float
    left: float
    width: float
    height: float

    def __hash__(self):
        return hash((self.top, self.left, self.width, self.height))

    def __eq__(self, other):
        if isinstance(other, Coordi):
            return self.top == other.top and self.left == other.left and self.width == other.width and self.height == other.height
        return False

class ItemInfo(BaseModel):
    is_photo: bool
    is_check: bool
    is_ex: bool
    text: str

