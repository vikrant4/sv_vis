import pandas as pd


def transform():
    transaction_data = pd.read_excel(
        'Transactions Gippsland modified NC.xlsx', sheet_name=1)
    transfer_data = pd.read_excel(
        'Transactions Gippsland modified NC.xlsx', sheet_name=2)
    disposal_data = pd.read_excel(
        'Transactions Gippsland modified NC.xlsx', sheet_name=3)

    transaction_data.to_csv('transaction_data.csv', index=False)
    transfer_data.to_csv('transfer_data.csv', index=False)
    disposal_data.to_csv('disposal_data.csv', index=False)


if __name__ == '__main__':
    transform()
