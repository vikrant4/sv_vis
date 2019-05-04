import sqlite3
import csv


def main():
    conn = sqlite3.connect('sv.db')
    try:
        create_db(conn)
        insert_data(conn)
    except Exception as e:
        print('ERROR:', e)
        conn.rollback()
    else:
        print('Commiting changes')
        conn.commit()
    finally:
        print('Closing connection')
        conn.close()


def create_db(conn):
    c = conn.cursor()
    # Creating facility_type table
    c.execute("""
        CREATE TABLE IF NOT EXISTS facility_type (
            type text primary key
        );
    """)
    # Creating facility table
    c.execute("""
        CREATE TABLE IF NOT EXISTS facility (
            code text primary key,
            name text not null,
            type text not null,
            region text not null,
            address text not null,
            suburb text not null,
            state text not null,
            postcode integer,
            latitude real not null,
            longitude real not null,
            active integer not null,
            foreign key(type) references facility_type(type)
        );
    """)
    # Creating transfer table
    c.execute("""
        CREATE TABLE IF NOT EXISTS transfer (
            trno integer primary key autoincrement,
            in_facility text not null,
            datetimein text not null,
            weightnett real not null default 0,
            item_group text not null,
            item_name text not null,
            inout text not null,
            quantity integer not null default 1,
            volume real,
            density real,
            kg_per_item real,
            tot_tonnes real,
            out_facility text,
            foreign key(in_facility) references facility(name),
            foreign key(out_facility) references facility(name)
        );
    """)
    print("Finished creating tables")


def insert_data(conn):
    c = conn.cursor()
    # Inserting facility type
    for ftype in ['Landfill', 'Reprocessor', 'RRC/TS']:
        c.execute("""
            INSERT OR IGNORE INTO facility_type ( type ) VALUES (?)
        """, [ftype])
    # Inserting facilities data
    facility_file = open('Facility List.csv')
    facility_csv_reader = csv.reader(facility_file)
    for index, row in enumerate(facility_csv_reader):
        active_map = {
            'TRUE': 1,
            'FALSE': 0
        }
        if index == 0:
            continue
        elif len(row[8]) == 0 | len(row[9]) == 0:
            continue
        row[10] = active_map[row[10].upper()]
        c.execute("""
            INSERT OR IGNORE INTO facility (
                type,
                name,
                code,
                region,
                address,
                suburb,
                state,
                postcode,
                latitude,
                longitude,
                active
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?);
        """, row)
    transfer_file = open('transaction_data.csv')
    transfer_csv_reader = csv.reader(transfer_file)
    for index, row in enumerate(transfer_csv_reader):
        if index == 0:
            continue
        try:
            c.execute("""
                INSERT INTO transfer (
                    in_facility,
                    datetimein,
                    weightnett,
                    item_group,
                    item_name,
                    inout,
                    quantity,
                    volume,
                    density,
                    kg_per_item,
                    tot_tonnes,
                    out_facility
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);
            """, row[2:])
        except Exception:
            print('Error happened for line below')
            print(row)
    print('Finished inserting values')


if __name__ == '__main__':
    main()
