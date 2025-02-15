import csv
import spacy
import os

# Load spaCy model for text processing
nlp = spacy.load('en_core_web_sm')

# Define a keyword-based category classifier with more categories
def categorize_article(text):
    categories = {
        "Politics": [
            "government", "election", "policy", "parliament", "politician", "vote", "campaign",
            "congress", "senate", "legislation", "minister", "democracy", "diplomacy", "president",
            "prime minister", "regulation", "sanction", "governor", "ambassador", "political party",
            "law", "constitution", "foreign affairs", "public policy", "republic", "opposition", "reform",
            "national security", "lawmaker", "executive order", "bipartisan", "corruption", "cabinet",
            "impeachment", "referendum", "socialism", "capitalism", "autocracy", "monarchy", "anarchy"
        ],
        "Technology": [
            "software", "AI", "cloud", "tech", "innovation", "internet", "digital", "robotics",
            "gadgets", "cybersecurity", "app", "startup", "blockchain", "cryptocurrency",
            "machine learning", "data science", "programming", "artificial intelligence", "VR",
            "augmented reality", "quantum computing", "algorithm", "automation", "IoT", "big data",
            "5G", "metaverse", "wearable tech", "smartphone", "biotechnology", "e-commerce"
        ],
        "Sports": [
            "football", "cricket", "tournament", "sports", "game", "match", "league", "athlete",
            "championship", "coach", "score", "Olympics", "World Cup", "medal", "competition",
            "team", "player", "stadium", "goal", "trophy", "sportsmanship", "federation", "rankings",
            "basketball", "tennis", "golf", "hockey", "rugby", "swimming", "athletics", "marathon"
        ],
        "Health": [
            "health", "medicine", "virus", "vaccine", "pandemic", "disease", "treatment", "doctor",
            "hospital", "wellness", "nutrition", "exercise", "mental health", "therapy", "healthcare",
            "COVID-19", "diagnosis", "surgery", "pharmaceutical", "epidemic", "public health",
            "medical research", "immunization", "telemedicine", "fitness", "diet", "alternative medicine",
            "yoga", "chronic disease", "health insurance"
        ],
        "Business": [
            "business", "economy", "stock", "finance", "market", "investment", "trade", "corporate",
            "startup", "entrepreneur", "merger", "acquisition", "revenue", "profit", "company",
            "CEO", "shares", "IPO", "economics", "banking", "inflation", "GDP", "debt", "interest rates",
            "currency", "industry", "taxes", "business strategy", "market analysis", "recession",
            "dividends", "capital", "global economy", "monetary policy", "venture capital", "hedge fund"
        ],
        "Human Interest": [
            "rescue", "life story", "personal", "human interest", "biography", "interview",
            "achievement", "inspiration", "community", "social", "volunteer", "activism", "charity",
            "hero", "kindness", "family", "struggle", "philanthropy", "care", "support", "help", "survivor",
            "humanitarian", "good samaritan", "nonprofit", "grassroots", "tribute", "hope", "resilience"
        ],
        "Lifestyle": [
            "lifestyle", "culture", "tradition", "food", "travel", "entertainment", "fashion", "art",
            "celebrity", "home", "relationship", "festival", "hobby", "interior design", "decor",
            "leisure", "music", "theater", "cinema", "celebrity", "wedding", "beauty", "trend", "tourism",
            "social media", "style", "luxury", "influencer", "spa", "well-being", "fitness", "hiking"
        ],
        "Food & Drink": [
            "food", "drink", "cuisine", "recipe", "restaurant", "cooking", "dining", "chef", "meal",
            "gourmet", "nutrition", "beverage", "wine", "beer", "dessert", "baking", "ingredients",
            "culinary", "fast food", "traditional dish", "organic", "healthy eating", "sustainable food",
            "street food", "vegetarian", "vegan", "farm-to-table", "craft beer", "coffee", "tea", "brunch"
        ],
        "Education": [
            "education", "school", "university", "learning", "student", "teacher", "course",
            "degree", "academic", "research", "curriculum", "scholarship", "classroom", "exam",
            "tuition", "education policy", "college", "admission", "virtual learning", "homeschooling",
            "STEM", "science fair", "higher education", "diploma", "literacy", "teacher training",
            "online courses", "MOOC", "SAT", "ACT", "extracurricular", "campus", "PhD", "master's"
        ],
        "Science": [
            "science", "research", "experiment", "discovery", "study", "theory", "scientist", "lab",
            "data", "technology", "physics", "biology", "chemistry", "astronomy", "geology",
            "environment", "space", "climate", "evolution", "genetics", "neuroscience",
            "artificial intelligence", "cosmology", "scientific method", "DNA", "molecular biology",
            "astronaut", "solar system", "quantum mechanics", "biophysics", "ecology", "microscope"
        ],
        "Environment": [
            "environment", "climate", "pollution", "conservation", "wildlife", "sustainability",
            "global warming", "carbon", "biodiversity", "ecosystem", "recycling", "waste",
            "natural disaster", "deforestation", "renewable energy", "solar", "wind energy",
            "fossil fuels", "greenhouse gases", "ocean", "water crisis", "wildfires", "habitat",
            "climate action", "energy efficiency", "plastic pollution", "sustainable living"
        ],
        "Crime": [
            "crime", "murder", "theft", "robbery", "assault", "arrest", "investigation", "fraud",
            "police", "court", "trial", "justice", "imprisonment", "terrorism", "violence",
            "homicide", "cybercrime", "drug trafficking", "law enforcement", "kidnapping",
            "domestic violence", "criminal", "legal", "conviction", "organized crime", "ransom",
            "scam", "forgery", "money laundering", "gang", "burglary", "identity theft"
        ]
    }

    # Process text using spaCy
    doc = nlp(text.lower())

    # Check for keywords in text
    for category, keywords in categories.items():
        if any(keyword in doc.text for keyword in keywords):
            return category

    return "Other"




# Path to your existing CSV file
csv_file_path = 'news_articles.csv'

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    print(f"File '{csv_file_path}' not found!")
else:
    # Read the existing data
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Store all rows in memory
        fieldnames = reader.fieldnames

        # Only add the 'Category' field if it's not already present
        if 'Category' not in fieldnames:
            fieldnames.append('Category')

        # Categorize articles based on the title and summary
        for row in rows:
            text = f"{row.get('Title', '')} {row.get('Summary', '')}"
            row['Category'] = categorize_article(text)

    # Write back to the same file with the updated rows
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write each row back to the file, now with the Category column
        for row in rows:
            writer.writerow(row)

    print(f"'Category' column successfully added and updated in '{csv_file_path}'")
