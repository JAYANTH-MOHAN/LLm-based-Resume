

"""I/O module of the ResumeParser."""

from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel, Field


class ProcessTimes(BaseModel):
    """The execution times of the different processes."""

    total: float
    pre_processing: float
    transcription: float
    extraction: float


class Timestamps(str, Enum):
    """Timestamps enum for the API."""

    seconds = "s"
    milliseconds = "ms"
    hour_minute_second = "hms"


class SubEQInfo(BaseModel):
    Institute: Union[str, None] = Field(
        ...,
        description="Name of the educational institute where the degree was earned; if not present, leave the field as "
                    "None."
    )
    From: Union[str, None] = Field(
        ...,
        description="Start date of the education or degree program; if not present, leave the field as None."
    )
    To: Union[str, None] = Field(
        ...,
        description="End date of the education or degree program; if not present, leave the field as None."
    )
    Degree: Union[str, None] = Field(
        ...,
        description="Type of degree obtained (e.g., Bachelor's, Master's, Ph.D.); if not present, leave the field as "
                    "None."
    )
    Specialization: Union[str, None] = Field(
        ...,
        description="Field of specialization or major for the degree; if not present, leave the field as None."
    )


class EQInfo(BaseModel):
    HighSchool: SubEQInfo
    HigherSecondary: SubEQInfo
    UnderGraduate: SubEQInfo
    PostGraduate: SubEQInfo


class WEInfo(BaseModel):
    Organization: Union[str, None] = Field(
        ...,
        description="Name of the organization where the candidate worked; if not present, leave the field as None."
    )
    FromDate: Union[str, None] = Field(
        ...,
        description="Start date of the candidate's employment; if not present, leave the field as None."
    )
    ToDate: Union[str, None] = Field(
        ...,
        description="End date of the candidate's employment; if not present, leave the field as None."
    )
    Position: Union[str, None] = Field(
        ...,
        description="The candidate's job position or title; if not present, leave the field as None."
    )
    Role: Union[str, None] = Field(
        ...,
        description="Description of the candidate's role or responsibilities; if not present, leave the field as None."
    )


class PCInfo(BaseModel):
    Email: Union[str, None] = Field(
        ...,
        description="Candidate's email address for communication; if not present, leave the field as None."
    )
    Linkedin: Union[str, None] = Field(
        ...,
        description="Candidate's LinkedIn profile URL or user name; if not present, leave the field as None."
    )
    Github: Union[str, None] = Field(
        ...,
        description="Candidate's GitHub profile URL or user name; if not present, leave the field as None."
    )


class ParserOutput(BaseModel):
    """Word model for the API."""

    Name: List[Union[str, None]] = Field(
        ...,
        description="Candidate's name usually in the beginning; if not present, leave the field as None."
    )
    PointOfCommunication: List[Union[PCInfo, None]] = Field(
        ...,
        description="Point of Communication information."
    )
    PhoneNumber: List[Union[str, None]] = Field(
        ...,
        description="A list of phone numbers; if not present, leave the field as None."
    )
    EducationQualification: EQInfo = Field(
        ...,
        description="Information about education qualifications."
    )
    WorkExperience: List[Union[WEInfo, None]] = Field(
        ...,
        description="A list of work experience information."
    )
    Skills: List[Union[str, None]] = Field(
        ...,
        description="A list of skills; if not present, leave the field as None."
    )


class BaseResponse(BaseModel):
    """Base response model, not meant to be used directly."""
    ParserResults: ParserOutput
    TimeStamps: str
    ProcessTimes: ProcessTimes


class ResumeParserResponse(BaseResponse):
    """Response model for the ResumeParser image file and url endpoint."""

    class Config:
        """Pydantic config class."""

        json_schema_extra = {
            "example": {
    "Name": [
      "Abhishek Test 7"
    ],
    "PointOfCommunication": [
      {
        "Email": "abhishek.Test7@publicissapient.com",
        "Linkedin": "linkedin.com/in/abhisheksuman887",
        "Github": "hackerrank.com/AviSuman"
      }
    ],
    "PhoneNumber": [
      "1100000000"
    ],
    "EducationQualification": {
      "HighSchool": {
        "Institute": "None",
        "From": "None",
        "To": "None",
        "Degree": "None",
        "Specialization": "None"
      },
      "HigherSecondary": {
        "Institute": "None",
        "From": "None",
        "To": "None",
        "Degree": "None",
        "Specialization": "None"
      },
      "UnderGraduate": {
        "Institute": "Heritage Institute of Technology, Kolkata, India",
        "From": "None",
        "To": "2019",
        "Degree": "Bachelor of Technology (BTech)",
        "Specialization": "Electronics And Communication Engineering"
      },
      "PostGraduate": {
        "Institute": "None",
        "From": "None",
        "To": "None",
        "Degree": "None",
        "Specialization": "None"
      }
    },
    "WorkExperience": [
      {
        "Organization": "Publicis Sapient",
        "FromDate": "March 2023",
        "ToDate": "Present",
        "Position": "Senior AssociateData Engineering L1",
        "Role": "Building Data warehouse which is used for reporting, analytics and reconciliation. HVR is used to extract data from multiple ERP sources like Oracle R12, Oracle Fusion, SAP and dump it in AWS S3. Databricks with AwS is used as unified data platform for transforming the data and loading it into Data warehouse. The transformed data is then used for reporting and analytical purposes."
      },
      {
        "Organization": "Tata Consultancy Services Pvt Ltd",
        "FromDate": "June 2019",
        "ToDate": "March 2023",
        "Position": "Data Engineer",
        "Role": "Worked mainly as a Data Engineer and experienced in designing, building, optimizing and maintaining data pipeline."
      },
      {
        "Organization": "SBIC Database Administration",
        "FromDate": "None",
        "ToDate": "None",
        "Position": "Oracle Database Administrator",
        "Role": "Maintaining and optimizing all the Production Databases."
      },
      {
        "Organization": "SBIC Vulnerability Management",
        "FromDate": "None",
        "ToDate": "None",
        "Position": "Linux Administrator",
        "Role": "Analyzing and mitigating vulnerabilities from servers."
      }
    ],
    "Skills": [
      "Cloud Infrastructure",
      "Data Analytics",
      "Data Engineering",
      "DE-Big Data",
      "DE-Data Warehouse and ETL",
      "SQL",
      "Python",
      "Apache Spark (RDD, Structured API's, Spark Streaming)",
      "Hadoop (HDFS, Hive, Sqoop, HBase)",
      "GCP ( Dataproc, GCS, Pub-Sub, Big Query)",
      "IAWS (EMR, S3, Glue, Lambda, Redshift)",
      "Databricks",
      "Snowflake",
      "Boto3",
      "Github",
      "Kafka"
    ]
  },
  "timestamps": "s",
  "process_times": {
    "total": 45.82109069824219,
    "pre_processing": 0.16302204132080078,
    "transcription": 22.233822107315063,
    "extraction": 23.422574996948242
  }
        }



class BaseRequest(BaseModel):
    """Base request model for the API."""

    timestamps: Timestamps = Timestamps.seconds

    class Config:
        """Pydantic config class."""

        json_schema_extra = {
            "example": {
                "timestamps": "s",
            }
        }


class ResumeParserRequest(BaseRequest):
    """Request model for the ResumeParser image file and url endpoint."""

    class Config:
        """Pydantic config class."""

        json_schema_extra = {
            "example": {
                "timestamps": "s",
            }
        }


class PongResponse(BaseModel):
    """Response model for the ping endpoint."""

    message: str

    class Config:
        """Pydantic config class."""

        json_schema_extra = {
            "example": {
                "message": "pong",
            },
        }


class Token(BaseModel):
    """Token model for authentication."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """TokenData model for authentication."""

    username: Optional[str] = None
