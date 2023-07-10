# from datetime import datetime
from typing import Dict
from typing import List

import requests
from loguru import logger

# from app import db
# from app.models.agents import AgentMetadata
# from app.models.agents import agent_metadata_schema
# from app.models.agents import agent_metadatas_schema
# from app.models.connectors import Connector
# from app.models.connectors import GraylogConnector
# from app.models.connectors import connector_factory
from app.services.Graylog.universal import UniversalService


class IndexService:
    """
    A service class that encapsulates the logic for pulling index data from Graylog
    """

    HEADERS: Dict[str, str] = {"X-Requested-By": "CoPilot"}

    def __init__(self):
        (
            self.connector_url,
            self.connector_username,
            self.connector_password,
        ) = UniversalService().collect_graylog_details("Graylog")

    def collect_indices(self):
        """
        Collects the indices that are managed by Graylog.

        Returns:
            list: A list containing the indices.
        """
        if (
            self.connector_url is None
            or self.connector_username is None
            or self.connector_password is None
        ):
            return {"message": "Failed to collect Graylog details", "success": False}

        managed_indices = self._collect_managed_indices()

        if managed_indices["success"]:
            index_names = self._extract_index_names(managed_indices)
            managed_indices["index_names"] = index_names

        return managed_indices

    def _collect_managed_indices(self) -> Dict[str, object]:
        """
        Collects the indices that are managed by Graylog.

        Returns:
            dict: A dictionary containing the success status, a message and potentially the indices.
        """
        try:
            managed_indices = requests.get(
                f"{self.connector_url}/api/system/indexer/indices",
                headers=self.HEADERS,
                auth=(self.connector_username, self.connector_password),
                verify=False,
            )
            return {
                "message": "Successfully collected managed indices",
                "success": True,
                "indices": managed_indices.json()["all"]["indices"],
            }
        except Exception as e:
            logger.error(f"Failed to collect managed indices: {e}")
            return {"message": "Failed to collect managed indices", "success": False}

    def _extract_index_names(self, response: Dict[str, object]) -> List[str]:
        """
        Extracts index names from the provided response.

        Args:
            response (dict): The dictionary containing the response.

        Returns:
            list: A list containing the index names.
        """
        index_names = list(response.get("indices", {}).keys())
        return index_names

    def delete_index(self, index_name: str) -> Dict[str, object]:
        """
        Deletes the specified index from Graylog.

        Args:
            index_name (str): The name of the index to delete.

        Returns:
            dict: A dictionary containing the response.
        """
        logger.info(f"Deleting index {index_name} from Graylog")
        if (
            self.connector_url is None
            or self.connector_username is None
            or self.connector_password is None
        ):
            return {"message": "Failed to collect Graylog details", "success": False}

        # Check if the index exists in Graylog
        managed_indices = self._collect_managed_indices()
        if managed_indices["success"]:
            index_names = self._extract_index_names(managed_indices)
            if index_name not in index_names:
                return {
                    "message": f"Index {index_name} is not managed by Graylog",
                    "success": False,
                }
            # Invoke _delete_index
            return self._delete_index(index_name)

        return {
            "message": f"Failed to delete index {index_name} from Graylog",
            "success": False,
        }

    def _delete_index(self, index_name: str) -> Dict[str, object]:
        """
        Deletes the specified index from Graylog.

        Args:
            index_name (str): The name of the index to delete.

        Returns:
            dict: A dictionary containing the response.
        """
        try:
            requests.delete(
                f"{self.connector_url}/api/system/indexer/indices/{index_name}",
                headers=self.HEADERS,
                auth=(self.connector_username, self.connector_password),
                verify=False,
            )
            return {
                "message": f"Successfully deleted index {index_name} from Graylog",
                "success": True,
            }
        except Exception as e:
            logger.error(f"Failed to delete index {index_name} from Graylog: {e}")
            return {
                "message": f"Failed to delete index {index_name} from Graylog. If this is the current index, "
                "it cannot be deleted.",
                "success": False,
            }
