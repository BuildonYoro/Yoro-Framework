from typing import Any, Dict, List, Literal, Optional, Tuple, Union


class UnstructuredIO:
    UNSTRUCTURED_MIN_VERSION = "0.10.30"

    def __init__(self):
        self._ensure_unstructured_version(self.UNSTRUCTURED_MIN_VERSION)

    def _ensure_unstructured_version(self, min_version: str) -> None:
        from packaging import version

        try:
            from unstructured.__version__ import __version__
        except ImportError as e:
            raise ImportError("Package `unstructured` not installed.") from e

        min_ver = version.parse(min_version)
        installed_ver = version.parse(__version__)

        if installed_ver < min_ver:
            raise ValueError(
                f"Require `unstructured>={min_version}`, you have {__version__}."
            )

    def parse_file_or_url(self, input_path: str, **kwargs: Any) -> Union[Any, List[Any]]:
        import os
        from urllib.parse import urlparse

        parsed_url = urlparse(input_path)
        is_url = all([parsed_url.scheme, parsed_url.netloc])

        if is_url:
            from unstructured.partition.html import partition_html

            try:
                elements = partition_html(url=input_path, **kwargs)
                return elements
            except Exception as e:
                raise Exception("Failed to parse the URL.") from e
        else:
            from unstructured.partition.auto import partition

            if not os.path.exists(input_path):
                raise FileNotFoundError(f"The file {input_path} was not found.")

            try:
                with open(input_path, "rb") as f:
                    elements = partition(file=f, **kwargs)
                    return elements
            except Exception as e:
                raise Exception("Failed to parse the unstructured file.") from e

    def clean_text_data(
        self,
        text: str,
        clean_options: Optional[List[Tuple[str, Dict[str, Any]]]] = None,
    ) -> str:
        from unstructured.cleaners.core import (
            bytes_string_to_string,
            clean_bullets,
            clean_dashes,
            clean_extra_whitespace,
            clean_non_ascii_chars,
            clean_ordered_bullets,
            clean_postfix,
            clean_prefix,
            clean_trailing_punctuation,
            group_broken_paragraphs,
            remove_punctuation,
            replace_unicode_quotes,
        )
        from unstructured.cleaners.translate import translate_text

        cleaning_functions = {
            "clean_extra_whitespace": clean_extra_whitespace,
            "clean_bullets": clean_bullets,
            "clean_ordered_bullets": clean_ordered_bullets,
            "clean_postfix": clean_postfix,
            "clean_prefix": clean_prefix,
            "clean_dashes": clean_dashes,
            "clean_trailing_punctuation": clean_trailing_punctuation,
            "clean_non_ascii_chars": clean_non_ascii_chars,
            "group_broken_paragraphs": group_broken_paragraphs,
            "remove_punctuation": remove_punctuation,
            "replace_unicode_quotes": replace_unicode_quotes,
            "bytes_string_to_string": bytes_string_to_string,
            "translate_text": translate_text,
        }

        if clean_options is None:
            clean_options = [
                ("replace_unicode_quotes", {}),
                ("clean_non_ascii_chars", {}),
                ("group_broken_paragraphs", {}),
                ("clean_extra_whitespace", {}),
            ]

        cleaned_text = text
        for func_name, params in clean_options:
            if func_name in cleaning_functions:
                cleaned_text = cleaning_functions[func_name](cleaned_text, **params)
            else:
                raise ValueError(
                    f"'{func_name}' is not a valid function in `unstructured`."
                )

        return cleaned_text

    def extract_data_from_text(
        self,
        text: str,
        extract_type: Literal[
            "extract_datetimetz",
            "extract_email_address",
            "extract_ip_address",
            "extract_ip_address_name",
            "extract_mapi_id",
            "extract_ordered_bullets",
            "extract_text_after",
            "extract_text_before",
            "extract_us_phone_number",
        ],
        **kwargs,
    ) -> Any:
        from unstructured.cleaners.extract import (
            extract_datetimetz,
            extract_email_address,
            extract_ip_address,
            extract_ip_address_name,
            extract_mapi_id,
            extract_ordered_bullets,
            extract_text_after,
            extract_text_before,
            extract_us_phone_number,
        )

        extraction_functions = {
            "extract_datetimetz": extract_datetimetz,
            "extract_email_address": extract_email_address,
            "extract_ip_address": extract_ip_address,
            "extract_ip_address_name": extract_ip_address_name,
            "extract_mapi_id": extract_mapi_id,
            "extract_ordered_bullets": extract_ordered_bullets,
            "extract_text_after": extract_text_after,
            "extract_text_before": extract_text_before,
            "extract_us_phone_number": extract_us_phone_number,
        }

        if extract_type not in extraction_functions:
            raise ValueError(f"Unsupported extract_type: {extract_type}")

        return extraction_functions[extract_type](text, **kwargs)

    def stage_elements(
        self,
        elements: List[Any],
        stage_type: Literal[
            "convert_to_csv",
            "convert_to_dataframe",
            "convert_to_dict",
            "dict_to_elements",
            "stage_csv_for_prodigy",
            "stage_for_prodigy",
            "stage_for_baseplate",
            "stage_for_datasaur",
            "stage_for_label_box",
            "stage_for_label_studio",
            "stage_for_weaviate",
        ],
        **kwargs,
    ) -> Union[str, List[Dict], Any]:
        from unstructured.staging import (
            base,
            baseplate,
            datasaur,
            label_box,
            label_studio,
            prodigy,
            weaviate,
        )

        staging_functions = {
            "convert_to_csv": base.convert_to_csv,
            "convert_to_dataframe": base.convert_to_dataframe,
            "convert_to_dict": base.convert_to_dict,
            "dict_to_elements": base.dict_to_elements,
            "stage_csv_for_prodigy": lambda els, **kw: prodigy.stage_csv_for_prodigy(
                els, kw.get("metadata", [])
            ),
            "stage_for_prodigy": lambda els, **kw: prodigy.stage_for_prodigy(
                els, kw.get("metadata", [])
            ),
            "stage_for_baseplate": baseplate.stage_for_baseplate,
            "stage_for_datasaur": lambda els, **kw: datasaur.stage_for_datasaur(
                els, kw.get("entities", [])
            ),
            "stage_for_label_box": lambda els, **kw: label_box.stage_for_label_box(
                els, **kw
            ),
            "stage_for_label_studio": lambda els, **kw: label_studio.stage_for_label_studio(
                els, **kw
            ),
            "stage_for_weaviate": weaviate.stage_for_weaviate,
        }

        if stage_type not in staging_functions:
            raise ValueError(f"Unsupported stage type: {stage_type}")

        return staging_functions[stage_type](elements, **kwargs)

    def chunk_elements(self, elements: List[Any], chunk_type: str, **kwargs) -> List[Any]:
        from unstructured.chunking.title import chunk_by_title

        chunking_functions = {
            "chunk_by_title": chunk_by_title,
        }

        if chunk_type not in chunking_functions:
            raise ValueError(f"Unsupported chunk type: {chunk_type}")

        return chunking_functions[chunk_type](elements, **kwargs)

    def run_s3_ingest(
        self, s3_url: str, output_dir: str, num_processes: int = 2, anonymous: bool = True
    ) -> None:
        from unstructured.ingest.interfaces import (
            FsspecConfig,
            PartitionConfig,
            ProcessorConfig,
            ReadConfig,
        )
        from unstructured.ingest.runner import S3Runner

        runner = S3Runner(
            processor_config=ProcessorConfig(
                verbose=True, output_dir=output_dir, num_processes=num_processes
            ),
            read_config=ReadConfig(),
            partition_config=PartitionConfig(),
            fsspec_config=FsspecConfig(remote_url=s3_url),
        )
        runner.run(anonymous=anonymous)

    def run_azure_ingest(
        self, azure_url: str, output_dir: str, account_name: str, num_processes: int = 2
    ) -> None:
        from unstructured.ingest.interfaces import (
            FsspecConfig,
            PartitionConfig,
            ProcessorConfig,
            ReadConfig,
        )
        from unstructured.ingest.runner import AzureRunner

        runner = AzureRunner(
            processor_config=ProcessorConfig(
                verbose=True, output_dir=output_dir, num_processes=num_processes
            ),
            read_config=ReadConfig(),
            partition_config=PartitionConfig(),
            fsspec_config=FsspecConfig(remote_url=azure_url),
        )
        runner.run(account_name=account_name)

    def run_github_ingest(
        self, repo_url: str, git_branch: str, output_dir: str, num_processes: int = 2
    ) -> None:
        from unstructured.ingest.interfaces import (
            PartitionConfig,
            ProcessorConfig,
            ReadConfig,
        )
        from unstructured.ingest.runner import GithubRunner

        runner = GithubRunner(
            processor_config=ProcessorConfig(
                verbose=True, output_dir=output_dir, num_processes=num_processes
            ),
            read_config=ReadConfig(),
            partition_config=PartitionConfig(),
        )
        runner.run(url=repo_url, git_branch=git_branch)

    def run_slack_ingest(
        self,
        channels: List[str],
        token: str,
        start_date: str,
        end_date: str,
        output_dir: str,
        num_processes: int = 2,
    ) -> None:
        from unstructured.ingest.interfaces import (
            PartitionConfig,
            ProcessorConfig,
            ReadConfig,
        )
        from unstructured.ingest.runner import SlackRunner

        runner = SlackRunner(
            processor_config=ProcessorConfig(
                verbose=True, output_dir=output_dir, num_processes=num_processes
            ),
            read_config=ReadConfig(),
            partition_config=PartitionConfig(),
        )
        runner.run(
            channels=channels, token=token, start_date=start_date, end_date=end_date
        )

    def run_discord_ingest(
        self, channels: List[str], token: str, output_dir: str, num_processes: int = 2
    ) -> None:
        from unstructured.ingest.interfaces import (
            PartitionConfig,
            ProcessorConfig,
            ReadConfig,
        )
        from unstructured.ingest.runner import DiscordRunner

        runner = DiscordRunner(
            processor_config=ProcessorConfig(
                verbose=True, output_dir=output_dir, num_processes=num_processes
            ),
            read_config=ReadConfig(),
            partition_config=PartitionConfig(),
        )
        runner.run(channels=channels, token=token)
