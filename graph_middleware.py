import copy
import httpx
import time
from kiota_http.middleware import BaseMiddleware
from kiota_abstractions.serialization.parse_node_factory_registry import ParseNodeFactoryRegistry
from msgraph.generated.models.external_connectors.connection_operation import ConnectionOperation
from msgraph.generated.models.external_connectors.connection_operation_status import ConnectionOperationStatus

class GraphMiddleware(BaseMiddleware):
    def __init__(self, delayMs: int) -> None:
        super().__init__()
        self.delayMs = delayMs

    @staticmethod
    def new_request(method: str, url: str, original_request) -> httpx.Request:
        new_request = httpx.Request(method=method, url=url, headers=original_request.headers, extensions=original_request.extensions)

        if method == "GET":
            new_request.headers["Content-Length"] = "0"

        new_request.context = original_request.context
        new_request.options = original_request.options
        return new_request

    async def send(self, request: httpx.Request, transport: httpx.AsyncBaseTransport) -> httpx.Response:
        request_before = copy.deepcopy(request)
        response: httpx.Response = await super().send(request, transport)
        location = response.headers.get("Location")
        if location:
            if "/operations/" not in location:
                return response

            time.sleep(self.delayMs / 1000)
            
            new_request = self.new_request("GET", location, request_before)
            return await self.send(new_request, transport)

        if "/operations/" not in str(request.url):
            return response
        
        if not response.is_success:
            return response

        body_bytes = response.read()
        parse_node = ParseNodeFactoryRegistry().get_root_parse_node("application/json", body_bytes)
        operation: ConnectionOperation = parse_node.get_object_value(ConnectionOperation.create_from_discriminator_value(parse_node))

        if operation.status == ConnectionOperationStatus.Inprogress:
            time.sleep(self.delayMs / 1000)
            new_request = self.new_request("GET", str(request_before.url), request_before)
            return await self.send(new_request, transport)
        else:
            return response
