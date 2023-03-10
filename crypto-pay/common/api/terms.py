import logging
import os
import test_resource.graphql as gql
import requests

logger = logging.getLogger(__name__)


class StagingTerms:
    terms_host = f"{os.environ['api_host']}"
    terms_gql = f"{terms_host}/graphql"

    @classmethod
    def accept_terms(cls, token: str, team_id: str):
        headers = {"Authorization": f"Bearer {token}"}
        variables = {"teamId": team_id}
        r = requests.post(
            url=cls.terms_gql, json={"query": gql.terms.ACCEPT_TERMS, "variables": variables}, headers=headers
        )
        if r.status_code == 200:
            t = r.json()
            if "errors" in t.keys():
                raise Exception(f"【Accept terms failed】： {str(t)}")
            logger.info(f"【Accept terms 】：{str(t)}")
        else:
            raise Exception(f"【Accept terms  failed】： {r.text}")
