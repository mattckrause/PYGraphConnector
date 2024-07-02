from graph_client import graph_client
from msgraph.generated.models.external_connectors.activity_settings import ActivitySettings
from msgraph.generated.models.external_connectors.display_template import DisplayTemplate
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.item_id_resolver import ItemIdResolver
from msgraph.generated.models.external_connectors.search_settings import SearchSettings
from msgraph.generated.models.external_connectors.url_match_info import UrlMatchInfo
from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.label import Label

#test function
async def get_user():
	user = await graph_client.users.by_user_id('mkrause@1d65k.onmicrosoft.com').get()
	if user:
		print(user.display_name)

#external Connection
external_connection = ExternalConnection(
    id="MKObjectSearch",
    name="Random Object Search",
    description="Random object search. Providing object description, a fun fact about the object, and a link to the wikipedia page for the object.",
    activity_settings=ActivitySettings(
        url_to_item_resolvers=[
            ItemIdResolver(
                odata_type="#microsoft.graph.externalConnectors.itemIdResolver",
                priority=1,
                item_id="{slug}",
                url_match_info=UrlMatchInfo(
                    base_urls=[
                        "https://en.wikipedia.org/wiki"
                    ],
                    url_pattern="/(?<slug>[^/]+)"
                )
            )
        ]
    ),
    search_settings=SearchSettings(
        search_result_templates=[
            DisplayTemplate(
                id="MKObjectSearch",
                priority=1
            )
        ]
    )
)

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
            name="Fun Fact",
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