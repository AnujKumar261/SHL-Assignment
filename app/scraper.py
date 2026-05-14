import json

sample_catalog = [
    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "description": "Measures Java programming and backend development skills.",
        "test_type": "Technical"
    },
    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq/",
        "description": "Measures workplace personality and behavioral preferences.",
        "test_type": "Personality"
    },
    {
        "name": "Verify Interactive G+",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-interactive-g-plus/",
        "description": "Measures general cognitive and reasoning ability.",
        "test_type": "Cognitive"
    },
    {
        "name": "Python (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
        "description": "Measures Python programming skills.",
        "test_type": "Technical"
    },
    {
        "name": "Agile Software Development",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/agile-software-development/",
        "description": "Measures agile software engineering knowledge.",
        "test_type": "Technical"
    },
    {
        "name": "Core Java (Entry Level)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level/",
        "description": "Measures entry-level Java programming ability.",
        "test_type": "Technical"
    },
    {
        "name": "SQL Server",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sql-server/",
        "description": "Measures SQL and database skills.",
        "test_type": "Technical"
    },
    {
        "name": "Leadership Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/leadership-report/",
        "description": "Evaluates leadership potential and management capability.",
        "test_type": "Leadership"
    }
]

with open(
    "data/shl_catalog.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(sample_catalog, f, indent=2)

print("SHL catalog created successfully.")