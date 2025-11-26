"""
Seed script to populate the database with initial Swedish vocabulary.
Run with: python -m src.scripts.seed_words
"""

import asyncio

from sqlalchemy import select

from src.db.session import async_session_maker
from src.models.word import Word

# Initial Swedish vocabulary - common words organized by CEFR level
SEED_WORDS = [
    # A1 - Basic vocabulary (most common words)
    {"swedish": "hej", "english": "hello, hi", "cefr_level": "A1", "part_of_speech": "interjection", "frequency_rank": 1, "example_sv": "Hej, hur mår du?", "example_en": "Hello, how are you?"},
    {"swedish": "ja", "english": "yes", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 2},
    {"swedish": "nej", "english": "no", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 3},
    {"swedish": "tack", "english": "thanks, thank you", "cefr_level": "A1", "part_of_speech": "interjection", "frequency_rank": 4, "example_sv": "Tack så mycket!", "example_en": "Thank you so much!"},
    {"swedish": "god", "english": "good", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 5},
    {"swedish": "dag", "english": "day", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 6, "example_sv": "God dag!", "example_en": "Good day!"},
    {"swedish": "natt", "english": "night", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 7},
    {"swedish": "morgon", "english": "morning", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 8},
    {"swedish": "kväll", "english": "evening", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 9},
    {"swedish": "jag", "english": "I", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 10},
    {"swedish": "du", "english": "you (singular)", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 11},
    {"swedish": "han", "english": "he", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 12},
    {"swedish": "hon", "english": "she", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 13},
    {"swedish": "vi", "english": "we", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 14},
    {"swedish": "de", "english": "they", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 15},
    {"swedish": "vara", "english": "to be", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 16, "example_sv": "Jag är glad.", "example_en": "I am happy."},
    {"swedish": "ha", "english": "to have", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 17},
    {"swedish": "göra", "english": "to do, to make", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 18},
    {"swedish": "säga", "english": "to say", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 19},
    {"swedish": "komma", "english": "to come", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 20},
    {"swedish": "gå", "english": "to go, to walk", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 21},
    {"swedish": "se", "english": "to see", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 22},
    {"swedish": "veta", "english": "to know (fact)", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 23},
    {"swedish": "vilja", "english": "to want", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 24},
    {"swedish": "kunna", "english": "can, to be able to", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 25},
    {"swedish": "ett", "english": "one, a/an (neuter)", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 26},
    {"swedish": "en", "english": "one, a/an (common)", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 27},
    {"swedish": "två", "english": "two", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 28},
    {"swedish": "tre", "english": "three", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 29},
    {"swedish": "fyra", "english": "four", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 30},
    {"swedish": "fem", "english": "five", "cefr_level": "A1", "part_of_speech": "numeral", "frequency_rank": 31},
    {"swedish": "hus", "english": "house", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 32, "example_sv": "Det är ett stort hus.", "example_en": "It is a big house."},
    {"swedish": "vatten", "english": "water", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 33},
    {"swedish": "mat", "english": "food", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 34},
    {"swedish": "kaffe", "english": "coffee", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 35},
    {"swedish": "te", "english": "tea", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 36},
    {"swedish": "mjölk", "english": "milk", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 37},
    {"swedish": "bröd", "english": "bread", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 38},
    {"swedish": "ost", "english": "cheese", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 39},
    {"swedish": "äpple", "english": "apple", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 40},

    # A1 - More common words
    {"swedish": "stor", "english": "big, large", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 41},
    {"swedish": "liten", "english": "small, little", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 42},
    {"swedish": "ny", "english": "new", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 43},
    {"swedish": "gammal", "english": "old", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 44},
    {"swedish": "ung", "english": "young", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 45},
    {"swedish": "vacker", "english": "beautiful", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 46},
    {"swedish": "glad", "english": "happy, glad", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 47},
    {"swedish": "ledsen", "english": "sad, sorry", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 48},
    {"swedish": "snäll", "english": "kind, nice", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 49},
    {"swedish": "lätt", "english": "easy, light", "cefr_level": "A1", "part_of_speech": "adjective", "frequency_rank": 50},

    # A1 - Family and people
    {"swedish": "familj", "english": "family", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 51},
    {"swedish": "mamma", "english": "mom, mother", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 52},
    {"swedish": "pappa", "english": "dad, father", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 53},
    {"swedish": "barn", "english": "child, children", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 54},
    {"swedish": "pojke", "english": "boy", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 55},
    {"swedish": "flicka", "english": "girl", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 56},
    {"swedish": "man", "english": "man, husband", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 57},
    {"swedish": "kvinna", "english": "woman", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 58},
    {"swedish": "vän", "english": "friend", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 59},

    # A1 - Places
    {"swedish": "hem", "english": "home", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 60, "example_sv": "Jag går hem.", "example_en": "I'm going home."},
    {"swedish": "skola", "english": "school", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 61},
    {"swedish": "arbete", "english": "work, job", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 62},
    {"swedish": "affär", "english": "store, shop", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 63},
    {"swedish": "stad", "english": "city, town", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 64},
    {"swedish": "land", "english": "country, land", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 65},
    {"swedish": "Sverige", "english": "Sweden", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 66},
    {"swedish": "svensk", "english": "Swedish (person), Swedish (adj)", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 67},
    {"swedish": "svenska", "english": "Swedish (language)", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 68},

    # A1 - Time
    {"swedish": "tid", "english": "time", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 69},
    {"swedish": "år", "english": "year", "cefr_level": "A1", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 70},
    {"swedish": "månad", "english": "month", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 71},
    {"swedish": "vecka", "english": "week", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 72},
    {"swedish": "timme", "english": "hour", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 73},
    {"swedish": "minut", "english": "minute", "cefr_level": "A1", "part_of_speech": "noun", "gender": "en", "frequency_rank": 74},
    {"swedish": "idag", "english": "today", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 75},
    {"swedish": "igår", "english": "yesterday", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 76},
    {"swedish": "imorgon", "english": "tomorrow", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 77},
    {"swedish": "nu", "english": "now", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 78},

    # A1 - Question words
    {"swedish": "vad", "english": "what", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 79, "example_sv": "Vad heter du?", "example_en": "What is your name?"},
    {"swedish": "var", "english": "where", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 80},
    {"swedish": "när", "english": "when", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 81},
    {"swedish": "hur", "english": "how", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 82, "example_sv": "Hur mår du?", "example_en": "How are you?"},
    {"swedish": "varför", "english": "why", "cefr_level": "A1", "part_of_speech": "adverb", "frequency_rank": 83},
    {"swedish": "vem", "english": "who", "cefr_level": "A1", "part_of_speech": "pronoun", "frequency_rank": 84},

    # A1 - Common verbs
    {"swedish": "äta", "english": "to eat", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 85, "example_sv": "Jag äter frukost.", "example_en": "I eat breakfast."},
    {"swedish": "dricka", "english": "to drink", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 86},
    {"swedish": "sova", "english": "to sleep", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 87},
    {"swedish": "läsa", "english": "to read", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 88},
    {"swedish": "skriva", "english": "to write", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 89},
    {"swedish": "prata", "english": "to talk, to speak", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 90},
    {"swedish": "lyssna", "english": "to listen", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 91},
    {"swedish": "köpa", "english": "to buy", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 92},
    {"swedish": "betala", "english": "to pay", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 93},
    {"swedish": "arbeta", "english": "to work", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 94},
    {"swedish": "bo", "english": "to live (reside)", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 95, "example_sv": "Jag bor i Stockholm.", "example_en": "I live in Stockholm."},
    {"swedish": "heta", "english": "to be called/named", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 96, "example_sv": "Jag heter Anna.", "example_en": "My name is Anna."},
    {"swedish": "tycka", "english": "to think (opinion)", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 97},
    {"swedish": "tänka", "english": "to think (cogitate)", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 98},
    {"swedish": "förstå", "english": "to understand", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 99},
    {"swedish": "behöva", "english": "to need", "cefr_level": "A1", "part_of_speech": "verb", "frequency_rank": 100},

    # A2 - More vocabulary
    {"swedish": "väder", "english": "weather", "cefr_level": "A2", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 101},
    {"swedish": "sol", "english": "sun", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 102},
    {"swedish": "regn", "english": "rain", "cefr_level": "A2", "part_of_speech": "noun", "gender": "ett", "frequency_rank": 103},
    {"swedish": "snö", "english": "snow", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 104},
    {"swedish": "varm", "english": "warm, hot", "cefr_level": "A2", "part_of_speech": "adjective", "frequency_rank": 105},
    {"swedish": "kall", "english": "cold", "cefr_level": "A2", "part_of_speech": "adjective", "frequency_rank": 106},
    {"swedish": "sommar", "english": "summer", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 107},
    {"swedish": "vinter", "english": "winter", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 108},
    {"swedish": "höst", "english": "autumn, fall", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 109},
    {"swedish": "vår", "english": "spring", "cefr_level": "A2", "part_of_speech": "noun", "gender": "en", "frequency_rank": 110},
]


async def seed_words():
    """Insert seed words into the database."""
    async with async_session_maker() as session:
        # Check if words already exist
        result = await session.execute(select(Word).limit(1))
        if result.scalar_one_or_none():
            print("Words already exist in database. Skipping seed.")
            return

        # Insert words
        words = [Word(**word_data) for word_data in SEED_WORDS]
        session.add_all(words)
        await session.commit()

        print(f"Successfully seeded {len(words)} Swedish words!")


if __name__ == "__main__":
    asyncio.run(seed_words())
