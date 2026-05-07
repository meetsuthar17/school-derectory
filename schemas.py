from pydantic import BaseModel


class StudentCreate(BaseModel):

    sid: int

    sname: str

    rollno: int

    did: int


    class Config:

        from_attributes = True