# External imports
import random  # nosec B311 # Standard random is sufficient for test data generation
from datetime import datetime

import pandas as pd
from loguru import logger


# All random usage in this file is for synthetic test data generation only
# nosec B311
def fake_it(store_data: bool = False) -> tuple[list[dict], list[dict]]:
    """
    Generate synthetic data for PRODUCT_NOMENCLATURE and TRANSACTIONS tables.
    This function creates two sets of test data:
    1. A product catalog with furniture and decoration items
    2. Transaction records spanning Dec 2018 to Jan 2020 with 3 transactions per month

    For better results in for production testing: https://docs.sdk.ydata.ai/latest/

    Args:
        store_data: If True, saves the generated data to CSV files in ./data/ directory

    Returns:
        Tuple containing two lists of dictionaries:
        - product_nomenclature_data: List of dictionaries with product metadata.
        - transaction_data: List of dictionaries with transaction details.
    """

    # Define synthetic data for the PRODUCT_NOMENCLATURE table
    # This represents a simple catalog of 6 products divided into two categories:
    # - MEUBLE (Furniture): Chair, Table, Sofa
    # - DECO (Decoration): Lamp, Painting, Rug
    product_nomenclature_data = [
        {"product_id": 1, "product_type": "MEUBLE", "product_name": "Chair"},
        {"product_id": 2, "product_type": "MEUBLE", "product_name": "Table"},
        {"product_id": 3, "product_type": "MEUBLE", "product_name": "Sofa"},
        {"product_id": 4, "product_type": "DECO", "product_name": "Lamp"},
        {"product_id": 5, "product_type": "DECO", "product_name": "Painting"},
        {"product_id": 6, "product_type": "DECO", "product_name": "Rug"},
    ]

    # If store_data is True, save the product catalog to a CSV file
    if store_data:
        product_nomenclature_df = pd.DataFrame(product_nomenclature_data)
        product_nomenclature_df.to_csv("./data/product_nomenclature.csv", index=False)
        logger.info("Product nomenclature data stored in ./data/product_nomenclature.csv")

    # Define the date range for generating transaction data
    # Transactions will span from December 2018 to January 2020
    start_date = datetime(2018, 12, 1)
    end_date = datetime(2020, 1, 31)

    # Initialize transaction data storage and counters
    transaction_data = []  # List to store all transactions
    transaction_id = 1  # Unique identifier for each transaction
    current_date = start_date  # Current date being processed

    # Generate transaction data with 3 transactions per month
    # This creates a consistent pattern of sales data for analysis
    while current_date <= end_date:
        for _ in range(3):  # Create 3 transactions for each month
            # Create a new transaction with randomized but realistic values
            transaction_data.append(
                {
                    "transaction_id": transaction_id,  # Unique identifier for the transaction
                    "date": current_date.strftime(
                        "%Y-%m-%d"
                    ),  # Transaction date in YYYY-MM-DD format
                    "order_id": random.randint(
                        1000, 9999
                    ),  # nosec B311 # Random order ID for test data (4-digit number)
                    "client_id": random.randint(
                        1, 50
                    ),  # nosec B311 # Random client ID for test data (50 different clients)
                    "prod_id": random.choice(
                        range(1, 7)
                    ),  # nosec B311 # Random product ID from our catalog (1-6)
                    "prod_price": round(
                        random.uniform(5, 500), 2  # nosec B311 # Random price between €5 and €500
                    ),  # Price rounded to 2 decimal places
                    "prod_qty": random.randint(
                        1, 10
                    ),  # nosec B311 # Random quantity between 1 and 10 units
                }
            )
            transaction_id += 1  # Increment transaction ID for the next entry

        # Move to the first day of the next month
        # This ensures we generate data for each month in our date range
        next_month = current_date.month % 12 + 1  # Calculate next month (1-12)
        next_year = (
            current_date.year if next_month != 1 else current_date.year + 1
        )  # Increment year if needed
        current_date = datetime(next_year, next_month, 1)  # Set to first day of next month

    # If store_data is True, save the transaction data to a CSV file
    if store_data:
        transactions_df = pd.DataFrame(transaction_data)
        transactions_df.to_csv("./data/transactions.csv", index=False)
        logger.info("Transactions data stored in ./data/transactions.csv")

    # Return both datasets for further use
    return product_nomenclature_data, transaction_data


if __name__ == "__main__":
    # When run as a script, generate and store the test data
    fake_it(store_data=True)
