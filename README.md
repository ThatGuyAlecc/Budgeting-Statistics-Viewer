# Budgeting Statistics Viewer

This project is a small budgeting statistics viewer. It takes a bank statement CSV export and compares your actual spending against budgets you define yourself. The result is a simple budget-vs-spending report plus a SQLite database containing the imported transactions.

## What it does

The pipeline runs in three stages:

1. `src/extract.py` reads the bank statement from `data/export.csv`, reads your budget values from `data/user_params.yaml`, and creates a fresh SQLite database in `data/database.db`.
2. `src/transform.py` parses the CSV, converts amounts to numbers, and assigns each transaction to a category using keyword matching on the recipient name.
3. `src/load.py` stores the transactions in SQLite and writes the comparison report to `output.txt`.

## Requirements

- Python 3
- Packages listed in `requirements.txt`
- A bank statement CSV saved as `data/export.csv`
- Budget values saved as `data/user_params.yaml`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Input files

### Bank statement CSV

The CSV file must be placed at `data/export.csv`. The current implementation expects a semicolon-separated file with at least these columns:

- `Saajan nimi`
- `Summa`

Amounts are parsed by replacing commas with dots before converting to numbers.

### Budget file

The budget file must be placed at `data/user_params.yaml`. The code accepts either of these formats:

```yaml
budgets:
  Food & Necessities: 300
  Transportation: 80
  Entertainment: 50
```

or a flat mapping:

```yaml
Food & Necessities: 300
Transportation: 80
Entertainment: 50
```

Missing or empty budget values are allowed, but they will be shown as placeholders in the report.

## How to run

From the project root, run:

```bash
python src/main.py
```

The script will recreate the database each time, import the transactions, and generate the report.

## Output

After a successful run you should see:

- `data/database.db` with the imported transactions
- `output.txt` in the project root with the budget comparison and totals

## Categories

Transactions are grouped using keyword matching on the recipient name. Current categories include:

- Food & Necessities
- Clothing
- Entertainment
- Transportation
- Sports & Fitness
- Other

Anything that does not match one of the known keywords is placed in `Other`.

## Important limitations

This project was tested only with S-Pankki bank statements and is only guaranteed to work with that CSV format. Differences in delimiter, column names, decimal formatting, or export layout may break parsing or classification.

Other practical notes:

- The SQLite database is dropped and recreated on every run.
- The report compares category spending against the budgets defined in `data/user_params.yaml`.
- Relative paths matter, so run the script from the repository root.

## Project structure

```text
.
├── data/
│   ├── README.md
│   ├── user_params.yaml
│   └── export.csv
├── requirements.txt
└── src/
    ├── extract.py
    ├── load.py
    ├── main.py
    └── transform.py
```