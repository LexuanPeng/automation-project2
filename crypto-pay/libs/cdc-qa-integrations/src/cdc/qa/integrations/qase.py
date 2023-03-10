from __future__ import annotations

import logging
from enum import Enum, unique

import qaseio
from qaseio.api import attachments_api, results_api, runs_api
from qaseio.model.get_results_filters_parameter import GetResultsFiltersParameter
from qaseio.model.result_create import ResultCreate
from qaseio.model.result_list_response import ResultListResponse
from qaseio.model.result_list_response_all_of_result import ResultListResponseAllOfResult
from qaseio.model.result_update import ResultUpdate
from qaseio.model.run_create import RunCreate
from qaseio.model.test_step_result_create import TestStepResultCreate

from .monkeypatch import qaseio as _qaseio  # noqa: F401

logger = logging.getLogger(__name__)


@unique
class TestRunResultStatus(Enum):
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    INVALID = "invalid"


class Qase:
    """
    qasio v3.0.0a3
    https://github.com/qase-tms/qase-python/tree/master/qaseio
    """

    STATUS = TestRunResultStatus

    def __init__(
        self,
        token: str,
        project_code: str,
        test_plan_id: str | int,
        test_run_id: str | int | None = None,
    ):
        self.project_code: str = project_code
        self.test_plan_id: int = int(test_plan_id)
        self.test_run_id: int | None = int(test_run_id) if test_run_id is not None else None

        self._config = qaseio.Configuration()
        self._config.api_key = {"TokenAuth": token}

        self._test_run_result_hash: str | None = None
        self._test_run_result_steps: list[TestStepResultCreate] = []

    def create_test_run(
        self,
        title: str,
        description: str | None = None,
        environment_id: int | None = None,
        test_cases: list[int] | None = None,
        is_autotest: bool = True,
        custom_field: dict = None,
    ) -> int:
        """Create a new Test Run and save the id in this object's property `test_run_id`.

        Args:
            title (str): Title of the Test Run.
            description (str, optional): Description of the Test Run. Defaults to None.
            environment_id (int, optional): Environment_id of the Test Run. Defaults to None.
            test_cases (list[int], optional): A list of Test Case ids of the Test Run. Overrides the setting of Test Plan if set. Defaults to None.
            is_autotest (bool, optional): Test run type. Defaults to True.
            custom_field (dict, optional): Test run custom field value, {<field_id_int>:<value/option_id_str>},
                e.g: {"90":"12", "96":"str value"}, must add all requirement fields

        Returns:
            int: The id of the Test Run created.
        """  # noqa: E501
        with qaseio.ApiClient(self._config) as api_client:
            runs_api_instance = runs_api.RunsApi(api_client)

            run_create_args = {
                "title": title,
                "is_autotest": is_autotest,
            }
            if description is not None:
                run_create_args["description"] = description
            if environment_id is not None:
                run_create_args["environment_id"] = environment_id
            if test_cases is not None:
                run_create_args["cases"] = test_cases
            else:
                run_create_args["plan_id"] = self.test_plan_id
            if custom_field:
                run_create_args["custom_field"] = custom_field

            run_create = RunCreate(**run_create_args)

            create_run_api_response = runs_api_instance.create_run(self.project_code, run_create)
            self.test_run_id = create_run_api_response.result.id
            logger.info(f"Test run created [{self.test_plan_id}]: {title} -> <{self.test_run_id}>")
            return self.test_run_id

    def complete_test_run(self):
        """Complete the current Test Run. Have no effect if current Test Run is already completed."""
        if self.test_run_id is None:
            raise ValueError("Test Run should be created before complete Test Run.")

        with qaseio.ApiClient(self._config) as api_client:
            runs_api_instance = runs_api.RunsApi(api_client)

            try:
                complete_run_api_response = runs_api_instance.complete_run(self.project_code, self.test_run_id)
                logger.debug(f"{complete_run_api_response=}")
            except qaseio.ApiException:
                logger.info(f"Test run was already completed! {self.test_run_id=}")

    def start_test_case(self, qase_id: str):
        """Start a Test Case recorded in Test Run Result and save the hash in this object.

        Args:
            qase_id (str): The id of the Test Case started.
        """
        if not self.test_run_id:
            raise ValueError("Test Run should be created before starting a Test Case.")

        with qaseio.ApiClient(self._config) as api_client:
            results_api_instance = results_api.ResultsApi(api_client)

            result_create = ResultCreate(
                case_id=int(qase_id.lstrip(f"{self.project_code}-")),
                status=TestRunResultStatus.IN_PROGRESS.value,
            )

            create_result_api_response = results_api_instance.create_result(
                self.project_code, self.test_run_id, result_create
            )
            logger.debug(create_result_api_response)
            self._test_run_result_hash = create_result_api_response["result"]["hash"]
            logger.info(f"Test Case started [{qase_id}] -> <{self._test_run_result_hash}>")

    def end_test_case(
        self,
        status: TestRunResultStatus,
        time_ms: int | None = None,
        comment: str | None = None,
        attachment_paths: list[str] | None = None,
    ):
        """End a Test Case in Test Run Result.

        Args:
            status (TestRunResultStatus): Final status of the Test Case.
            time_ms (int, optional): Execution time (in ms) of the Test Case. Defaults to None.
            comment (str, optional): Comment on the Test Case. Defaults to None.
            attachment_paths (list[str], optional): A list of paths of attachments. Defaults to None.
        """
        if not self.test_run_id:
            raise ValueError("Test Run should be created before ending Test Case.")

        if not self._test_run_result_hash:
            raise ValueError("Test Case should be started before ending Test Case.")

        with qaseio.ApiClient(self._config) as api_client:
            results_api_instance = results_api.ResultsApi(api_client)

            result_update_args = {
                "status": status.value,
                "steps": self._test_run_result_steps,
            }
            if time_ms:
                result_update_args["time_ms"] = time_ms
            if comment:
                result_update_args["comment"] = comment
            if attachment_paths:
                result_update_args["attachments"] = self._upload_attachments(attachment_paths)

            result_update = ResultUpdate(**result_update_args)

            update_result_api_response = results_api_instance.update_result(
                self.project_code,
                self.test_run_id,
                self._test_run_result_hash,
                result_update,
            )
            logger.debug(update_result_api_response)
            logger.info(f"Test Case ended <{self._test_run_result_hash}>: {status}")
            logger.debug(f"Cached steps: {self._test_run_result_steps}")
            self._test_run_result_hash = None
            self._test_run_result_steps = []

    def end_test_step(
        self,
        status: TestRunResultStatus,
        comment: str | None = None,
        attachment_paths: list[str] | None = None,
        update_to_qase: bool = True,
    ):
        """End Test Step in Test Run Result.

        Args:
            status (TestRunResultStatus): Final status of the Test Step.
            comment (str, optional): Comment on the Test Step. Defaults to None.
            attachment_paths (list[str], optional): A list of paths of attachments. Defaults to None.
            update_to_qase (bool, optional): update step result to qase. Defaults to True.
        """
        if not self.test_run_id:
            raise ValueError("Test Run should be created before ending Test Step.")

        if not self._test_run_result_hash:
            raise ValueError("Test Case should be started before ending Test Step.")

        position = 1 + len(self._test_run_result_steps)

        step_args = {
            "position": position,
            "status": status.value,
        }
        if comment:
            step_args["comment"] = comment
        if attachment_paths:
            step_args["attachments"] = self._upload_attachments(attachment_paths)

        step = TestStepResultCreate(**step_args)

        self._test_run_result_steps.append(step)
        logger.debug(f"Add step: {step}")

        if update_to_qase:
            with qaseio.ApiClient(self._config) as api_client:
                results_api_instance = results_api.ResultsApi(api_client)
                result_update = ResultUpdate(
                    status=self.STATUS.IN_PROGRESS.value,
                    steps=self._test_run_result_steps,
                )

                api_response = results_api_instance.update_result(
                    self.project_code,
                    self.test_run_id,
                    self._test_run_result_hash,
                    result_update,
                )
                logger.debug(api_response)
                logger.info(f"Test Step ended <{self._test_run_result_hash}>[{position}]: {status}")

    def _upload_attachments(self, file_paths: list[str]) -> list[str]:
        """Upload multiple files as attachments to Qase.

        Args:
            file_paths (list[str]): A list of paths of the files to be uploaded.

        Returns:
            list[str]: A list of attachment hashes of the uploaded files.
        """
        # * Note that the API provided by Qase already allows uploading up to 20 files at once,
        # * but we chose to upload the files one by one in case an upload fails.
        with qaseio.ApiClient(self._config) as api_client:
            attachments_api_instance = attachments_api.AttachmentsApi(api_client)

            hashes = []

            for file_path in file_paths:
                try:
                    file = open(file_path, "rb")
                    upload_attachment_api_response = attachments_api_instance.upload_attachment(
                        self.project_code, file=[file]
                    )
                    hash = upload_attachment_api_response["result"][0]["hash"]
                    logger.info(f"File uploaded: '{file_path}' -> <{hash}>")
                    hashes.append(hash)
                except FileNotFoundError:
                    logger.critical(f"File not found in: '{file_path}'")

            return hashes

    def get_test_run_failed_cases(self) -> list[int]:
        """get test run all failed cases list id"""
        if self.test_run_id is None:
            raise ValueError("Test Run should be created before complete Test Run.")

        with qaseio.ApiClient(self._config) as api_client:
            results_api_instance = results_api.ResultsApi(api_client)

            try:
                # get all failed cases
                failed_case_ids = []
                total_failed = float("inf")
                got_count = 0

                limit = 100
                offset = 0
                filters = GetResultsFiltersParameter(status="failed", run=str(self.test_run_id))
                while got_count < total_failed:
                    result_list: ResultListResponse = results_api_instance.get_results(
                        self.project_code,
                        limit=limit,
                        offset=offset,
                        filters=filters,
                    )
                    failed_cases: ResultListResponseAllOfResult = result_list["result"]
                    for result in failed_cases.entities:
                        if result.case_id not in failed_case_ids:
                            failed_case_ids.append(result.case_id)

                    total_failed = failed_cases.filtered
                    got_count += failed_cases.count
                    offset += limit

                # filter passed cases
                limit = 100
                offset = 0
                pass_case_ids = []
                for case_id in failed_case_ids:
                    # get case results
                    filters = GetResultsFiltersParameter(run=str(self.test_run_id), case_id=str(case_id))
                    case_result: ResultListResponse = results_api_instance.get_results(
                        self.project_code,
                        limit=limit,
                        offset=offset,
                        filters=filters,
                    )

                    for result in case_result.result.entities:
                        if result.status == "Passed":
                            pass_case_ids.append(result.case_id)
                            break

                return list(set(failed_case_ids) - set(pass_case_ids))
            except qaseio.ApiException as e:
                logger.info(f"get failed case error! {str(e)}")
            except Exception as e:
                raise Exception(f"get qase failed cases list failed! {str(e)}")
