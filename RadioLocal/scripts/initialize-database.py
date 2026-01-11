import pymongo
import os
from dotenv import load_dotenv

# Load .env file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# Get MongoDB connection string
mongo_url = os.getenv('DB_URL')
if not mongo_url:
    raise ValueError("Missing DB_URL in .env file")

client = pymongo.MongoClient(mongo_url)
db = client['radiodb']


def get_station_collection(company_id):
    return db[f"stations_{company_id}"]


def add_station(name, description, logo_url, stream_url, company_id, user_id):
    collection = get_station_collection(company_id)
    station_data = {
        'name': name,
        'description': description,
        'logo_url': logo_url,
        'stream_url': stream_url,
        'user_id': user_id
    }
    return collection.insert_one(station_data)


# --------- NEW: Check existing collections ----------
def check_existing_collections():
    """Return a list of existing station collections."""
    existing = []
    for name in db.list_collection_names():
        if name.startswith("stations_"):
            existing.append(name)
    return existing


def ask_overwrite(existing):
    """Prompt user if they want to overwrite existing collections."""
    print("⚠️  The following collections already exist:")
    for col in existing:
        print("  -", col)

    while True:
        choice = input("\nDo you want to OVERWRITE them? (y/n): ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            print("Exiting without changes.")
            exit(0)
        else:
            print("Please type 'y' or 'n'.")


# ----------------------------------------------------


def initialize_database():
    # Check existing collections first
    existing = check_existing_collections()

    if existing:
        if ask_overwrite(existing):
            print("\n🗑 Dropping old collections...")
            for col in existing:
                db[col].drop()
            print("✔ Old collections removed.\n")

    print("📦 Inserting initial station data...")

    # Insert sample data
    add_station(
        name="Murski Val",
        description="Radio Murski val sem glas severovzhodne Slovenije že od leta 1958",
        logo_url="https://static.mytuner.mobi/media/tvos_radios/442/radio-murski-val-946-fm.fb8d3624.png",
        stream_url="https://stream.murskival.si",
        company_id="1",
        user_id="7ecb758c-1cdc-4580-8fab-7c2de78d3948"
    )

    add_station(
        name="Radio Banovina",
        description="Slušaju svi - slušajte i vi!",
        logo_url="https://www.radio-banovina.hr/wp-content/uploads/2015/01/logo-120_00000.png",
        stream_url="https://audio.radio-banovina.hr:9998/stream",
        company_id="1",
        user_id="7ecb758c-1cdc-4580-8fab-7c2de78d3948"
    )

    add_station(
        name="Radio Sorisso",
        description="Più giovane che mai",
        logo_url="https://www.sorrriso.it/wp-content/uploads/2018/09/logo-radio-sorrriso.png",
        stream_url="https://ice02.fluidstream.net/sorriso.mp3",
        company_id="2",
        user_id="bcf08366-39e9-4611-bc2d-18ddaefdec9b"
    )

    add_station(
        name="Radio Romantica",
        description="Radio Romantica è una radio IP, DAB FM e WEB. Tutta la musica che ti ha fatto innamorare",
        logo_url="https://www.radioromantica.net/images/romantica500.png",
        stream_url="https://nr12.newradio.it:8656/stream",
        company_id="2",
        user_id="bcf08366-39e9-4611-bc2d-18ddaefdec9b"
    )

    print("✅ Database initialized with sample stations.")


def main():
    initialize_database()


if __name__ == "__main__":
    main()