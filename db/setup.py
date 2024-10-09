import weaviate
from weaviate.classes.config import Property, DataType, Configure

DEPARTMENTS = [
    {
        "name": "Operations",
        "description": "Responsible for managing the logistical and functional aspects of the organization's services, focusing on efficiency, productivity, and quality control.",
    },
    {
        "name": "Customer Service",
        "description": "Dedicated to handling customer interactions and ensuring high satisfaction through various support channels. This department manages feedback and resolves customer queries.",
    },
    {
        "name": "Research and Development",
        "description": "Focused on innovation and improvement of products, services, and processes through continuous research, experimentation, and development.",
    },
    {
        "name": "Marketing",
        "description": "Strategizes and executes plans to promote the organization's products or services, enhances brand awareness, and drives sales through various marketing channels.",
    },
    {
        "name": "Human Resources",
        "description": "Manages recruitment, employee relations, training, and development, ensuring the organization has a skilled and motivated workforce.",
    },
    {
        "name": "Finance",
        "description": "Responsible for managing the organization's financial resources, including budgeting, forecasting, financial reporting, and strategic financial planning.",
    },
    {
        "name": "IT and Technology",
        "description": "Handles the organization's technological infrastructure, including hardware, software, networks, and cybersecurity, ensuring efficient operations and data security.",
    },
    {
        "name": "Sales",
        "description": "Focuses on generating revenue through direct sales of products or services, maintaining client relationships, and achieving sales targets through effective strategies.",
    },
    {
        "name": "Legal",
        "description": "Ensures compliance with laws and regulations, manages legal risks, drafts contracts, and provides legal advice and support across the organization.",
    },
]

with weaviate.connect_to_local() as client:
    if not client.collections.exists("Chunks"):
        client.collections.create(
            "Chunks",
            properties=[
                Property(name="department", data_type=DataType.TEXT),
                Property(name="filename", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT, vectorize_property_name=True),
            ]
        )
        print("Created collection Chunks!")
        
    if not client.collections.exists("Images"):
        client.collections.create(
            "Images",
            properties=[
                Property(name="name", data_type=DataType.TEXT),
                Property(name="path", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
            ]
        )
        print("Created collection Images!")
        
    if not client.collections.exists("Tables"):
        client.collections.create(
            "Tables",
            properties=[
                Property(name="name", data_type=DataType.TEXT),
                Property(name="path", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
            ]
        )
        print("Created collection Tables!")
        
    if not client.collections.exists("Departments"):
        departments_collection = client.collections.create(
            "Departments",
            properties=[
                Property(name="name", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
            ]
        )
        departments_collection.data.insert_many(DEPARTMENTS)
        print("Created collection Departments!")
