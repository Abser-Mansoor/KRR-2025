# Gold-standard candidates for 20 Questions AI
# Diverse set covering multiple continents, occupations, and time periods

SAMPLE_CANDIDATES = [
    # Scientists
    {"name": "Albert Einstein", "gender": "male", "occupation": "physicist", "nationality": "german", "field": "physics", "fictional": False, "alive": False, "continent": "Europe", "country": "Germany", "known_for": "theory of relativity"},
    {"name": "Marie Curie", "gender": "female", "occupation": "physicist", "nationality": "polish", "field": "physics", "fictional": False, "alive": False, "continent": "Europe", "country": "Poland", "known_for": "radioactivity"},
    {"name": "Isaac Newton", "gender": "male", "occupation": "physicist", "nationality": "british", "field": "physics", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "laws of motion"},
    {"name": "Charles Darwin", "gender": "male", "occupation": "naturalist", "nationality": "british", "field": "biology", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "evolution"},
    {"name": "Stephen Hawking", "gender": "male", "occupation": "physicist", "nationality": "british", "field": "physics", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "black holes"},
    
    # Artists
    {"name": "Leonardo da Vinci", "gender": "male", "occupation": "artist", "nationality": "italian", "field": "art", "fictional": False, "alive": False, "continent": "Europe", "country": "Italy", "known_for": "mona lisa"},
    {"name": "Pablo Picasso", "gender": "male", "occupation": "artist", "nationality": "spanish", "field": "art", "fictional": False, "alive": False, "continent": "Europe", "country": "Spain", "known_for": "cubism"},
    {"name": "Vincent van Gogh", "gender": "male", "occupation": "artist", "nationality": "dutch", "field": "art", "fictional": False, "alive": False, "continent": "Europe", "country": "Netherlands", "known_for": "starry night"},
    {"name": "Frida Kahlo", "gender": "female", "occupation": "artist", "nationality": "mexican", "field": "art", "fictional": False, "alive": False, "continent": "Americas", "country": "Mexico", "known_for": "self portraits"},
    
    # Musicians
    {"name": "Wolfgang Amadeus Mozart", "gender": "male", "occupation": "composer", "nationality": "austrian", "field": "music", "fictional": False, "alive": False, "continent": "Europe", "country": "Austria", "known_for": "classical music"},
    {"name": "Ludwig van Beethoven", "gender": "male", "occupation": "composer", "nationality": "german", "field": "music", "fictional": False, "alive": False, "continent": "Europe", "country": "Germany", "known_for": "symphony no 9"},
    {"name": "Michael Jackson", "gender": "male", "occupation": "singer", "nationality": "american", "field": "music", "fictional": False, "alive": False, "continent": "Americas", "country": "United States", "known_for": "thriller"},
    {"name": "Beyoncé", "gender": "female", "occupation": "singer", "nationality": "american", "field": "music", "fictional": False, "alive": True, "continent": "Americas", "country": "United States", "known_for": "lemonade"},
    
    # Writers
    {"name": "William Shakespeare", "gender": "male", "occupation": "playwright", "nationality": "british", "field": "literature", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "hamlet"},
    {"name": "J.K. Rowling", "gender": "female", "occupation": "author", "nationality": "british", "field": "literature", "fictional": False, "alive": True, "continent": "Europe", "country": "United Kingdom", "known_for": "harry potter"},
    {"name": "Mark Twain", "gender": "male", "occupation": "author", "nationality": "american", "field": "literature", "fictional": False, "alive": False, "continent": "Americas", "country": "United States", "known_for": "tom sawyer"},
    
    # Leaders
    {"name": "Napoleon Bonaparte", "gender": "male", "occupation": "emperor", "nationality": "french", "field": "military", "fictional": False, "alive": False, "continent": "Europe", "country": "France", "known_for": "napoleonic wars"},
    {"name": "Mahatma Gandhi", "gender": "male", "occupation": "activist", "nationality": "indian", "field": "politics", "fictional": False, "alive": False, "continent": "Asia", "country": "India", "known_for": "nonviolent resistance"},
    {"name": "Nelson Mandela", "gender": "male", "occupation": "politician", "nationality": "south african", "field": "politics", "fictional": False, "alive": False, "continent": "Africa", "country": "South Africa", "known_for": "anti-apartheid"},
    {"name": "Abraham Lincoln", "gender": "male", "occupation": "politician", "nationality": "american", "field": "politics", "fictional": False, "alive": False, "continent": "Americas", "country": "United States", "known_for": "emancipation"},
    {"name": "Cleopatra", "gender": "female", "occupation": "pharaoh", "nationality": "egyptian", "field": "monarchy", "fictional": False, "alive": False, "continent": "Africa", "country": "Egypt", "known_for": "ruling egypt"},
    {"name": "Queen Elizabeth II", "gender": "female", "occupation": "monarch", "nationality": "british", "field": "monarchy", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "longest reign"},
    
    # Philosophers
    {"name": "Aristotle", "gender": "male", "occupation": "philosopher", "nationality": "greek", "field": "philosophy", "fictional": False, "alive": False, "continent": "Europe", "country": "Greece", "known_for": "logic"},
    {"name": "Confucius", "gender": "male", "occupation": "philosopher", "nationality": "chinese", "field": "philosophy", "fictional": False, "alive": False, "continent": "Asia", "country": "China", "known_for": "confucianism"},
    
    # Sports
    {"name": "Michael Jordan", "gender": "male", "occupation": "basketball player", "nationality": "american", "field": "sports", "fictional": False, "alive": True, "continent": "Americas", "country": "United States", "known_for": "nba"},
    {"name": "Lionel Messi", "gender": "male", "occupation": "footballer", "nationality": "argentinian", "field": "sports", "fictional": False, "alive": True, "continent": "Americas", "country": "Argentina", "known_for": "barcelona"},
    {"name": "Serena Williams", "gender": "female", "occupation": "tennis player", "nationality": "american", "field": "sports", "fictional": False, "alive": True, "continent": "Americas", "country": "United States", "known_for": "tennis"},
    {"name": "Muhammad Ali", "gender": "male", "occupation": "boxer", "nationality": "american", "field": "sports", "fictional": False, "alive": False, "continent": "Americas", "country": "United States", "known_for": "boxing"},
    
    # Actors
    {"name": "Marilyn Monroe", "gender": "female", "occupation": "actress", "nationality": "american", "field": "film", "fictional": False, "alive": False, "continent": "Americas", "country": "United States", "known_for": "hollywood"},
    {"name": "Charlie Chaplin", "gender": "male", "occupation": "actor", "nationality": "british", "field": "film", "fictional": False, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "silent films"},
    
    # Fictional Characters
    {"name": "Sherlock Holmes", "gender": "male", "occupation": "detective", "nationality": "british", "field": "none", "fictional": True, "alive": False, "continent": "Europe", "country": "United Kingdom", "known_for": "logical reasoning"},
    {"name": "Harry Potter", "gender": "male", "occupation": "wizard", "nationality": "british", "field": "none", "fictional": True, "alive": True, "continent": "Europe", "country": "United Kingdom", "known_for": "defeating voldemort"},
    {"name": "James Bond", "gender": "male", "occupation": "spy", "nationality": "british", "field": "none", "fictional": True, "alive": True, "continent": "Europe", "country": "United Kingdom", "known_for": "007"},
]
