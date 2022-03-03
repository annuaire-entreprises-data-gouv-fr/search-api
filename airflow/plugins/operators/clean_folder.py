import os
import shutil
from typing import Optional

from airflow.models import BaseOperator


class CleanFolderOperator(BaseOperator):
    """
    Clean tmp folder
    :param folder_path: path of folder to clean
    :type folder_path: str

    """

    supports_lineage = True

    template_fields = ("folder_path",)

    def __init__(
        self,
        *,
        folder_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.folder_path = folder_path

    def execute(self, context):
        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            shutil.rmtree(self.folder_path)
