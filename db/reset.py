import weaviate

collections_to_be_removed = ["Chunks", "Images", "Tables", "Departments"]

with weaviate.connect_to_local() as client:
    for collection_name in collections_to_be_removed:
        if client.collections.exists(collection_name):
            client.collections.delete(collection_name)
            print(f"Removed collection {collection_name}")
