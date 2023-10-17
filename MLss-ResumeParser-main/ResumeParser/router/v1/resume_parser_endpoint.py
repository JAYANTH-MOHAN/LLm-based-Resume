

import asyncio
import os
import json
from typing import List, Union
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi import status as http_status
from loguru import logger

from ResumeParser.config import settings
from ResumeParser.dependencies import resume_parser
from ResumeParser.models import ResumeParserRequest, ResumeParserResponse
from ResumeParser.utils import (
    delete_file,
    save_file_locally,
    get_file_name
)

router = APIRouter()


@router.post(
    "", response_model=Union[ResumeParserResponse, str], status_code=http_status.HTTP_200_OK
)
async def inference_with_parser(  # noqa: C901
    background_tasks: BackgroundTasks,
    timestamps: str = Form("s"),  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
) -> ResumeParserResponse:
    """Inference endpoint with audio file."""
    filename, req_id = get_file_name(settings.storage_dir, file.filename.split(".")[-1])

    await save_file_locally(filename=filename, file=file)

    data = ResumeParserRequest(
        timestamps=timestamps,
    )

    task = asyncio.create_task(
        resume_parser.process_input(
            filepath=filename,
            timestamps_format=data.timestamps
        )
    )
    result = await task

    # enable it to delete the stored files
    # background_tasks.add_task(delete_file, filepath=filename)

    if isinstance(result, Exception):
        logger.error(f"Error: {result}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(result),
        )
    else:
        parser_result, process_times = result
        j_parser_result = json.dumps(parser_result)
        if os.path.exists(settings.log_file):
            pass
        else:
            with open(settings.log_file, "a+") as api_calls_log_file:
                api_calls_log_file.write(",".join([
                    "req_id", "file_name", "json_file_name"]) + "\n")

        with open(settings.log_file, "a+") as api_calls_log_file:
            json_filename, _ = get_file_name(settings.storage_dir, "json")
            out_file = open(json_filename, "w")
            json.dump(j_parser_result, out_file, indent=4)
            out_file.close()
            api_calls_log_file.write(
                ",".join([
                    req_id, filename, json_filename]) + "\n")

        return ResumeParserResponse(
            ParserResults=parser_result,
            TimeStamps=data.timestamps,
            ProcessTimes=process_times,
        )
