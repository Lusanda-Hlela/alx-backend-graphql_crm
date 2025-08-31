# crm/cron.py
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM is alive\n")
    try:
        transport = RequestsHTTPTransport(
            url="http://127.0.0.1:8000/graphql/", verify=True, retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("query { hello }")
        response = client.execute(query)
        print("GraphQL endpoint response:", response)
    except Exception as e:
        print(f"Error querying GraphQL endpoint: {e}")


def update_low_stock():
    """
    Calls GraphQL mutation updateLowStockProducts and logs results.
    """
    try:
        transport = RequestsHTTPTransport(
            url="http://127.0.0.1:8000/graphql/", verify=True, retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql(
            """
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    id
                    name
                    stock
                }
                message
            }
        }
        """
        )

        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]

        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - Low stock products updated:\n")
            for product in updated_products:
                log_file.write(f"{product['name']} - Stock: {product['stock']}\n")
            log_file.write("\n")

        print(f"{len(updated_products)} products restocked successfully!")

    except Exception as e:
        print(f"Error updating low stock products: {e}")
