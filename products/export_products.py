import pandas as pd


products = [
    {
        "id": 31,
        "name": "Samsung Galaxy S21",
        "price": 699.00,
        "stock": 45,
        "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s21-5g.jpg",
        "category": "Electronics",
        "description": "Flagship 2021 smartphone with 6.2″ Dynamic AMOLED 2X display, Exynos/Snapdragon chipset, triple rear camera, IP68 water resistance",
        "subcategory": "Smartphones"
    },
    {
        "id": 32,
        "name": "Samsung Galaxy S23",
        "price": 799.00,
        "stock": 40,
        "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23.jpg",
        "category": "Electronics",
        "description": "2023 flagship with Snapdragon 8 Gen 2, 6.1″ AMOLED display, 50 MP main camera, AI-enhanced photography, narrow bezels, IP68",
        "subcategory": "Smartphones"
    },
    {
        "id": 33,
        "name": "Samsung Galaxy A06",
        "price": 129.00,
        "stock": 80,
        "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-a06.jpg",
        "category": "Electronics",
        "description": "Entry-level smartphone with 6.7″ HD+ display, MediaTek Helio G85, 50 MP camera, 5000 mAh battery—great budget pick",
        "subcategory": "Smartphones"
    },
    {
        "id": 35,
        "name": "Toyota Corolla 2016",
        "price": 14900.00,
        "stock": 5,
        "image_url": "https://example.com/toyota-corolla-2016.jpg",
        "category": "Automobile",
        "description": "Reliable compact sedan with 132–140 hp 1.8 L engine, ~31 mpg combined, spacious interior, strong safety record, dependability award",
        "subcategory": "Sedan"
    },
    {
        "id": 34,
        "name": "Toyota Camry 2020",
        "price": 24900.00,
        "stock": 3,
        "image_url": "https://www.toyota.com/imgix/responsive/images/gallery/photos/2020/camry/2020-camry-gallery-01.jpg?auto=format%2Ccompress&fit=crop&h=500&w=1000&q=80",
        "category": "Automobile",
        "description": "Mid-size sedan with 203 hp 2.5 L engine, ~28 mpg combined, spacious interior, advanced safety features, strong resale value",
        "subcategory": "Sedan"
    },
    {"id": 36, "name": "Nissan Pathfinder 2025", "price": 36400.00, "stock": 10, "image_url": "https://cdn.nissanusa.com/pathfinder-2025/galaxy.jpg", "category": "Automobile", "description": "3‑row midsize SUV with 3.5 L V6 (284 hp, or 295 hp in Rock Creek), 9‑speed auto, seats 7–8, up to 6,000 lb towing, terrain modes, ProPILOT Assist, top safety ratings", "subcategory": ""},
    {"id": 37, "name": "Google Pixel 5", "price": 699.00, "stock": 60, "image_url": "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-5-5g.jpg", "category": "Electronics", "description": "6″ OLED 90 Hz display, Snapdragon 765G, 8 GB RAM, dual cameras, 4080 mAh battery, IP68", "subcategory": ""},
    {"id": 38, "name": "OnePlus 7T", "price": 599.00, "stock": 35, "image_url": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-7t.jpg", "category": "Electronics", "description": "6.55″ Fluid AMOLED 90 Hz, Snapdragon 855+, triple camera, 30 W fast charge", "subcategory": ""},
    {"id": 39, "name": "itel A06", "price": 99.00, "stock": 100, "image_url": "https://fdn2.gsmarena.com/vv/bigpic/itel-a06.jpg", "category": "Electronics", "description": "Android 14 Go, quad-core 1.4 GHz, 2 GB + virtual RAM, 5000 mAh battery, budget", "subcategory": ""},
    {"id": 40, "name": "Tecno Spark 10", "price": 129.00, "stock": 80, "image_url": "https://fdn2.gsmarena.com/vv/bigpic/tecno-spark-10.jpg", "category": "Electronics", "description": "6.6″ HD+ 90 Hz, Helio G37, 8 GB RAM, 50 MP camera, 5000 mAh battery", "subcategory": ""},
    {"id": 41, "name": "iPhone 6s", "price": 199.00, "stock": 30, "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-6s.jpg", "category": "Electronics", "description": "4.7″ Retina HD, A9 chip, 12 MP camera, 3D Touch, headphone jack", "subcategory": ""}
]


df = pd.DataFrame(products)
df.to_csv("products.csv", index=False)
print("CSV file 'products.csv' created successfully!")
