from jist.authentication_mode import AuthenticationMode
from jist.structure import Structure
import jist.utils.http_service as http
from jist.specs import (
    PatResponse,
    ConfigResponse
)
from jist.rest_resources import rest_api
from jist.jist_operation import JistOperation
import jist.jist_cache as jist_cache


class JIST:
    def __init__(
            self,
            hostname: str,
            username: str = None,
            password: str = None,
            pat: str = None,
            authentication_mode=AuthenticationMode.PAT):
        # Initialized HTTP service to setup request data
        http.init(hostname, username, password, pat, authentication_mode)
        # Setup public fields
        self.rest_api: rest_api = rest_api

        # Proceed with PAT authetication request when:
        # - PAT auth mode is selected
        # - PAT token is not supplied, thus it must be requested
        # - username and password are supplied to retrieve valid PAT token
        if ((authentication_mode is AuthenticationMode.PAT)
                and (not http.jira_pat)
                and (username and password)):
            auth_operation = self.request_pat(username, password)

            if auth_operation.failed:
                # Raise exception if authentication request failed
                raise Exception(
                    (
                        f"PAT authentication failed:"
                        f" {auth_operation.error.message}"
                    )
                )

    def request_pat(
            self,
            username: str,
            password: str) -> JistOperation[PatResponse]:
        token_operation = self.rest_api.get_pat(username, password)

        if token_operation.succeeded:
            http.set_pat(token_operation.content.raw_token)

        return token_operation

    def load_config(self) -> JistOperation[ConfigResponse]:
        config_operation = self.rest_api.get_config()

        if config_operation.failed:
            return config_operation

        jist_cache.load_config(config_operation.content)

        return config_operation

    def structure(self, structure_id: int) -> Structure:
        return Structure(structure_id)
