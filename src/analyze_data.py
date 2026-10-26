
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "data/raw/transactions.csv"


def analyze_dataset():
    df = pd.read_csv(DATA_FILE)

    print("\n--- DATASET OVERVIEW ---")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE TRANSACTIONS ---")
    print(df["transaction_id"].duplicated().sum())

    print("\n--- FRAUD LABEL DISTRIBUTION ---")
    print(df["fraud_label"].value_counts())
    print("\nLabel percentages:")
    print((df["fraud_label"].value_counts(normalize=True) * 100).round(2))

    print("\n--- AMOUNT STATISTICS ---")
    print(df.groupby("fraud_label")["amount"].describe())

    print("\n--- LABEL CONSISTENCY ---")
    print(
        pd.crosstab(
            df["is_suspicious"],
            df["fraud_label"],
            margins=True,
        )
    )

    df.groupby("fraud_label")["amount"].plot(
        kind="hist",
        alpha=0.6,
        bins=30,
        legend=True,
    )
    plt.title("Transaction Amount Distribution by Label")
    plt.xlabel("Transaction Amount (INR)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze_dataset()
