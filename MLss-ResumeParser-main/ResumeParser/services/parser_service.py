

"""ResumeParser Service module that handle all AI interactions."""

import asyncio
import functools
import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Tuple

from ResumeParser.logging import time_and_tell
from ResumeParser.services.pre_processing_service import PreProcessingService
from ResumeParser.services.transcribe_service import TranscribeService
from ResumeParser.services.extraction_service import ExtractionService


class ResumeParserService(ABC):
    """Base ResumeParser Service module that handle all AI interactions and batch processing."""

    def __init__(self) -> None:
        """Initialize the ResumeParser Service.

        This class is not meant to be instantiated. Use the subclasses instead.
        """
        self.device = "cpu"
        self.num_cpus = os.cpu_count()

        self.queues = None  # the queue to store requests
        self.queue_locks = None  # the locks to access the queues
        self.needs_processing = (
            None  # the flag to indicate if the queue needs processing
        )
        self.needs_processing_timer = None  # the timer to schedule processing

        self.device_index = [0]

        @abstractmethod
        async def process_input(self) -> None:
            """Process the input request by creating a task and adding it to the appropriate queues."""
            raise NotImplementedError("This method should be implemented in subclasses.")


class ResumeAsyncService(ResumeParserService):
    """ResumeParser Service module for async endpoints."""

    def __init__(
        self,
        debug_mode: bool,
    ) -> None:

        super().__init__()

        self.services: dict = {
            "pre_processing": PreProcessingService(),
            "transcription": TranscribeService(
            ),
            "extraction": ExtractionService(),
        }
        self.debug_mode = debug_mode

    async def inference_warmup(self) -> None:
        """Warmup the machine by loading the models."""
        sample_path = Path(__file__).parent.parent / "assets/sample.pdf"

        await self.process_input(
            filepath=str(sample_path),
            timestamps_format="s"
        )

    async def process_input(  # noqa: C901
        self,
        filepath: str,
        timestamps_format: str
    ) -> Tuple[dict, dict]:

        task = {
            "input": filepath,
            "timestamps_format": timestamps_format,
            "pre_processing_result": None,
            "pre_processing_done": asyncio.Event(),
            "transcription_result": None,
            "transcription_done": asyncio.Event(),
            "extraction_result": None,
            "extraction_done": asyncio.Event(),
            "process_times": {},
        }

        start_process_time = time.time()

        # pre-processing
        asyncio.get_event_loop().run_in_executor(
            None,
            functools.partial(
                self.process_pre_processing, task, self.debug_mode
            ),
        )
        await task["pre_processing_done"].wait()

        # transcription
        asyncio.get_event_loop().run_in_executor(
            None,
            functools.partial(
                self.process_transcription, task, self.debug_mode
            ),
        )
        await task["transcription_done"].wait()

        # post-processing
        asyncio.get_event_loop().run_in_executor(
            None, functools.partial(self.process_extraction, task)
        )
        await task["extraction_done"].wait()

        result: dict = task.pop("extraction_result")
        process_times: Dict[str, float] = task.pop("process_times")
        process_times["total"]: float = time.time() - start_process_time

        del task  # Delete the task to free up memory

        return result, process_times

    def process_pre_processing(
        self, task: dict, debug_mode: bool
    ) -> None:

        result, process_time = time_and_tell(
            lambda: self.services["pre_processing"](
                task["input"],
            ),
            func_name="pre_processing",
            debug_mode=debug_mode,
        )

        task["process_times"]["pre_processing"] = process_time
        task["pre_processing_result"] = result
        task["pre_processing_done"].set()
        return None

    def process_transcription(
        self, task: dict, debug_mode: bool
    ) -> None:

        result, process_time = time_and_tell(
            lambda: self.services["transcription"](
                task["pre_processing_result"]["ip_file"]
            ),
            func_name="transcription",
            debug_mode=debug_mode,
        )

        task["process_times"]["transcription"] = process_time
        task["transcription_result"] = result
        task["transcription_done"].set()
        return None

    def process_extraction(self, task: dict) -> None:

        total_extraction_time = 0

        final_results, process_time = time_and_tell(
            lambda: self.services["extraction"](
                text=task["transcription_result"]["extracted_text"],
            ),
            func_name="extraction",
            debug_mode=self.debug_mode,
        )
        total_extraction_time += process_time

        task["process_times"]["extraction"] = total_extraction_time
        task["extraction_result"] = final_results
        task["extraction_done"].set()
        return None
