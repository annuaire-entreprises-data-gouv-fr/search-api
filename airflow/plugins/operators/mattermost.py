from typing import Dict, Optional

from airflow.models import BaseOperator
import requests

class MattermostOperator(BaseOperator):
    """
    Executes a mattermost message
    :param mattermost_endpoint: endpoint mattersmost for bot
    :type mattermost_endpoint: str
    :param text: text for mattermost message
    :type text: str
    :param image_url: url of image to post
    :type image_url: str
    """

    supports_lineage = True

    template_fields = ('mattermost_endpoint', 'text', 'image_url')

    def __init__(
        self,
        *,
        mattermost_endpoint: Optional[str] = None,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.mattermost_endpoint = mattermost_endpoint
        self.text = text
        self.image_url = image_url

    def execute(self, context):
        if not self.mattermost_endpoint or not self.text:
            raise ValueError("Not enough information to send message")

        data = {}
        data['text'] = self.text
        if self.image_url:
            data['attachments'] = [
            { 
                'image_url': self.image_url
            }
        ]

        r = requests.post(self.mattermost_endpoint, json = data)
