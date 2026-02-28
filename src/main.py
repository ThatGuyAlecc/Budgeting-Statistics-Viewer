from extract import init_db, get_stats_per_category, get_total_stats
from load import load_data
from transform import transform_data


def main():
    conn = init_db()
    if conn is None:
        print("Failed to initialize database. Exiting.")
        return

    df = transform_data()
    load_data(df, conn)
    print(get_stats_per_category(conn))
    print(get_total_stats(conn))
    conn.close()

    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()

