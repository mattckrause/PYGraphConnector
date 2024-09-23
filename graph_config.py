import sys
import logging
from graph_client import graph_client
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.label import Label
from msgraph.generated.models.external_connectors.access_type import AccessType
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.external_item import ExternalItem
from msgraph.generated.models.external_connectors.properties import Properties

logging.basicConfig(filename='graphconnector.log')
logger = logging.getLogger(__name__)

async def create_external_connection(id: str, name: str, description: str) -> None:
    logger.info("Creating external connection")
    external_connection = ExternalConnection(
        id=id,
        name=name,
        description=description,
    )

    try:
        await graph_client.external.connections.post(body=external_connection)
        logger.info("External connection created successfully")
    except Exception as e:
        logger.error(f"There was an error creating the connection: {e}")
        sys.exit(1)

async def create_schema(id: str) -> None:
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
                is_retrievable=True,
                IsContent=True
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
    logger.info("Creating schema...")
    try:
        await graph_client.external.connections.by_external_connection_id(id).schema.patch(schema)
        logger.info("Schema created successfully")
    except Exception as e:
        logger.error(f"There was an error creating the schema: {e}")
        sys.exit(1)

async def write_objects(id: str, json_content) -> None:
    for obj in json_content:
        print(f"Creating object: {obj['Name']}")
        logger.info(f"Creating object: {obj['Name']}")
        object_body = ExternalItem(
            id=obj["ID"],
            properties=Properties(
                additional_data={
                    "Name": obj["Name"],
                    "Description": obj["Description"],
                    "FunFact": obj["FunFact"],
                    "URL": obj["WikipediaLink"]
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
            print("Object created successfully...")
            logger.info("Object created successfully...")
        except Exception as e:
            print(f"Error on {obj['Name']}: {e}")
            logger.error(f"Error on {obj['Name']}: {e}")