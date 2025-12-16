import sys
import traceback
from external_service import user_mapping
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.access_type import AccessType
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.label import Label
from msgraph.generated.models.external_connectors.external_item import ExternalItem
from msgraph.generated.models.external_connectors.properties import Properties


async def create_external_connection(id: str, name: str, description: str, tenantID: str, graph_client) -> None:
    print("Creating external connection")
    external_connection = ExternalConnection(
        id=id,
        name=name,
        description=description,
    )

    try:
        print("calling graph client creation process...")
        await graph_client.external.connections.post(body=external_connection)
        print("External connection created successfully")
    except Exception as e:
        print(f"There was an error creating the connection: {e}")
        sys.exit(1)

async def remove_external_connection(id: str, graph_client) -> None:
    print("Removing external connection")
    try:
        await graph_client.external.connections.by_external_connection_id(id).delete()
        print("External connection removed successfully")
    except Exception as e:
        print(f"There was an error removing the connection: {e}")
        sys.exit(1)

async def create_schema(id: str, graph_client) -> None:
    schema = Schema(
        base_type="microsoft.graph.externalItem",
        properties=[
            Property_(
                name="Name",
                type=PropertyType.String,
                is_queryable=True,
                is_searchable=True,
                is_retrievable=True,
                labels=[
                    Label.Title
                ]
            ),
            Property_(
                name="Description",
                type=PropertyType.String,
                is_queryable=True,
                is_searchable=True,
                is_retrievable=True
            ),
            Property_(
                name="FunFact",
                type=PropertyType.String,
                is_retrievable=True
            ),
            Property_(
                name="url",
                type=PropertyType.String,
                is_retrievable=True,
                labels=[
                    Label.Url
                ]
            )
        ]
    )
    print("creating schema...")
    try:
        await graph_client.external.connections.by_external_connection_id(id).schema.patch(schema)
        print('Schema created successfully')
    except Exception:
        print(traceback.format_exc())
        sys.exit(1)

async def write_objects(id: str, json_content, graph_client) -> None:
    print("graph_config - Writing objects...")
    for obj in json_content:
        print(f"graph_config - Creating object: {obj['Name']}")
        object_body = ExternalItem(
            id=obj["ID"],
            properties=Properties(
                additional_data={
                    "Name": obj["Name"],
                    "Description": obj["Description"],
                    "FunFact": obj["FunFact"],
                    "URL": obj["WikipediaLink"],
                    "Icon": "https://gcfileserv.blob.core.windows.net/image/MKlogo.png"
                }
            ),
            acl=[
                Acl(
                    type=AclType.Everyone,
                    value="everyone",
                    access_type=AccessType.Grant
                )
            ]
        )
        try:
            await graph_client.external.connections.by_external_connection_id(id).items.by_external_item_id(object_body.id).put(object_body)
            print("graph_config - Object created successfully...")
        except Exception as e:
            print(f"graph_config - Error on {obj['Name']}: {e}")