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
        print(f"Creating new request: {new_request.method} {new_request.url}")
        return new_request

    async def send(self, request: httpx.Request, transport: httpx.AsyncBaseTransport) -> httpx.Response:
        request_before = copy.deepcopy(request)
        print("request URL: ", request_before)

        response: httpx.Response = await super().send(request, transport)
        location = response.headers.get("Location")

        print("checking response location...")
        if location:
            if "/operations/" not in location:
                print(f"/operations/ not in location: {response}")
                return response

            print("Operation in progress... waiting")
            time.sleep(self.delayMs / 1000)
            
            new_request = self.new_request("GET", location, request_before)
            print(f"new request: {new_request}")
            return await self.send(new_request, transport)

        print("checking response URL...")
        print(f"type of request.url: {type(request.url)}")
        print(f"Request URL: {request.url}")

        if "/operations/" not in str(request.url):
            print("not a job")
            return response

        print("line 54")

        if response.is_success: #changed from not
            print("response is success")
            return response

        print("line 60")
        body_bytes = response.read()
        print(f"Response body: {body_bytes}")
        parse_node = ParseNodeFactoryRegistry().get_root_parse_node("application/json", body_bytes)
        operation: ConnectionOperation = parse_node.get_object_value(ConnectionOperation.create_from_discriminator_value(parse_node))

        if operation.status == ConnectionOperationStatus.Inprogress:
            print("Operation in progress... waiting")
            time.sleep(self.delayMs / 1000)
            new_request = self.new_request("GET", str(request_before.url), request_before)
            return await self.send(new_request, transport)
        else:
            return response
