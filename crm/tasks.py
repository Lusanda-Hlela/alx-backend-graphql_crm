import requests
from celery import shared_task
from datetime import datetime


def log_report(customers, orders, revenue):
    """Append CRM report to log file with timestamp."""
    with open("/tmp/crm_report_log.txt", "a") as log_file:
        log_file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            f"- Report: {customers} customers, {orders} orders, {revenue} revenue\n"
        )


@shared_task
def generate_crm_report():
    """
    Celery task that queries the GraphQL API to generate a CRM report.
    Summarizes total customers, orders, and revenue.
    Logs results to /tmp/crm_report_log.txt.
    """
    query = """
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql", json={"query": query}, timeout=10
        )

        if response.status_code == 200:
            data = response.json().get("data", {})
            customers = data.get("customersCount", 0)
            orders = data.get("ordersCount", 0)
            revenue = data.get("totalRevenue", 0)
            log_report(customers, orders, revenue)
        else:
            with open("/tmp/crm_report_log.txt", "a") as log_file:
                log_file.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"- Failed to fetch CRM report: {response.status_code}\n"
                )

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                f"- Error generating CRM report: {str(e)}\n"
            )
