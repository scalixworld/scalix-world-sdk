from enum import Enum


class CrawlerCategory(str, Enum):
    AI_AGENT = "ai_agent"
    AI_ASSISTANT = "ai_assistant"
    AI_CODING_AGENT = "ai_coding_agent"
    AI_DATA_PROVIDER = "ai_data_provider"
    AI_TRAINING_SCRAPER = "ai_training_scraper"
    CUSTOM = "custom"
    SEARCH_ENGINE = "search_engine"

    def __str__(self) -> str:
        return str(self.value)
