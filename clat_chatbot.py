import re
from typing import Dict, List, Tuple
import random

class CLATChatbot:
    def __init__(self):
        # Knowledge base
        self.knowledge_base = {
            "syllabus": {
                "english": ["Reading Comprehension", "Grammar", "Vocabulary"],
                "gk": ["Current Affairs", "Static GK", "Legal GK"],
                "legal_aptitude": ["Legal Principles", "Legal Maxims", "Case Laws"],
                "logical_reasoning": ["Analytical Reasoning", "Logical Reasoning"],
                "mathematics": ["Basic Mathematics", "Data Interpretation"]
            },
            "pattern": {
                "total_questions": 150,
                "english": 28,
                "gk": 35,
                "legal_aptitude": 35,
                "logical_reasoning": 28,
                "mathematics": 24
            },
            "cutoffs": {
                "nls": {
                    "2023": 98.5,
                    "2022": 98.2,
                    "2021": 97.8
                },
                "nlud": {
                    "2023": 97.8,
                    "2022": 97.5,
                    "2021": 97.0
                },
                "nlu": {
                    "2023": 96.5,
                    "2022": 96.2,
                    "2021": 95.8
                }
            },
            "faqs": {
                "exam_duration": "2 hours",
                "negative_marking": "0.25 marks for each wrong answer",
                "total_marks": "150",
                "mode": "Computer-based test (CBT)"
            }
        }
        
        # Intent patterns
        self.intent_patterns = {
            "syllabus": [
                r"syllabus",
                r"what.*syllabus",
                r"topics",
                r"subjects",
                r"what.*study"
            ],
            "pattern": [
                r"pattern",
                r"questions",
                r"marks",
                r"how many.*questions",
                r"total.*questions"
            ],
            "cutoff": [
                r"cutoff",
                r"cut-off",
                r"cut off",
                r"last year.*cutoff",
                r"previous.*cutoff"
            ],
            "faq": [
                r"duration",
                r"time",
                r"negative marking",
                r"total marks",
                r"mode",
                r"how.*conducted"
            ]
        }
        
        # Response templates
        self.response_templates = {
            "syllabus": {
                "section": "The {section} section includes: {topics}",
                "all": "CLAT syllabus includes:\n{content}"
            },
            "pattern": {
                "section": "The {section} section has {count} questions",
                "total": "CLAT has a total of {count} questions"
            },
            "cutoff": {
                "college": "The cutoff for {college} in {year} was {cutoff} percentile",
                "all": "Here are the cutoffs for top NLUs:\n{content}"
            },
            "faq": {
                "general": "The {topic} for CLAT is {answer}"
            }
        }

    def _extract_intent(self, query: str) -> str:
        """Extract the intent from the user query."""
        query = query.lower()
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent
        return "unknown"

    def _extract_entities(self, query: str) -> Dict[str, str]:
        """Extract relevant entities from the query."""
        entities = {}
        
        # Extract year if present
        year_match = re.search(r"20\d{2}", query)
        if year_match:
            entities["year"] = year_match.group()
        
        # Extract college names
        college_keywords = {
            "nls": ["nls", "nlsiu", "bangalore"],
            "nlud": ["nlud", "delhi"],
            "nlu": ["nlu", "jodhpur"]
        }
        
        for college, keywords in college_keywords.items():
            if any(keyword in query.lower() for keyword in keywords):
                entities["college"] = college
                break
        
        # Extract section names
        section_keywords = {
            "english": ["english", "language"],
            "gk": ["gk", "general knowledge"],
            "legal_aptitude": ["legal", "aptitude"],
            "logical_reasoning": ["logical", "reasoning"],
            "mathematics": ["math", "mathematics"]
        }
        
        for section, keywords in section_keywords.items():
            if any(keyword in query.lower() for keyword in keywords):
                entities["section"] = section
                break
        
        return entities

    def _generate_response(self, intent: str, entities: Dict[str, str], query: str) -> str:
        """Generate response based on intent and entities."""
        if intent == "unknown":
            return "I'm sorry, I couldn't understand your query. Could you please rephrase it?"
        
        if intent == "syllabus":
            if "section" in entities:
                section = entities["section"]
                topics = ", ".join(self.knowledge_base["syllabus"][section])
                return self.response_templates["syllabus"]["section"].format(
                    section=section,
                    topics=topics
                )
            else:
                content = []
                for section, topics in self.knowledge_base["syllabus"].items():
                    content.append(f"{section.title()}: {', '.join(topics)}")
                return self.response_templates["syllabus"]["all"].format(
                    content="\n".join(content)
                )
        
        elif intent == "pattern":
            if "section" in entities:
                section = entities["section"]
                count = self.knowledge_base["pattern"][section]
                return self.response_templates["pattern"]["section"].format(
                    section=section,
                    count=count
                )
            else:
                return self.response_templates["pattern"]["total"].format(
                    count=self.knowledge_base["pattern"]["total_questions"]
                )
        
        elif intent == "cutoff":
            if "college" in entities and "year" in entities:
                college = entities["college"]
                year = entities["year"]
                cutoff = self.knowledge_base["cutoffs"][college][year]
                return self.response_templates["cutoff"]["college"].format(
                    college=college.upper(),
                    year=year,
                    cutoff=cutoff
                )
            else:
                content = []
                for college, years in self.knowledge_base["cutoffs"].items():
                    latest_year = max(years.keys())
                    content.append(f"{college.upper()}: {years[latest_year]} (2023)")
                return self.response_templates["cutoff"]["all"].format(
                    content="\n".join(content)
                )
        
        elif intent == "faq":
            for topic, answer in self.knowledge_base["faqs"].items():
                if topic.replace("_", " ") in query.lower():
                    return self.response_templates["faq"]["general"].format(
                        topic=topic.replace("_", " "),
                        answer=answer
                    )
            return "I'm sorry, I couldn't find specific information about that in our FAQs."

    def get_response(self, query: str) -> str:
        """Process the user query and return a response."""
        intent = self._extract_intent(query)
        entities = self._extract_entities(query)
        return self._generate_response(intent, entities, query)

# Example usage
if __name__ == "__main__":
    chatbot = CLATChatbot()
    
    # Sample queries
    queries = [
        "What is the syllabus for CLAT 2025?",
        "How many questions are there in the English section?",
        "Give me last year's cut-off for NLSIU Bangalore.",
        "What is the exam duration?",
        "Tell me about the mathematics syllabus",
        "What was the cutoff for NLU Jodhpur in 2022?"
    ]
    
    print("CLAT Chatbot Demo\n" + "="*50)
    for query in queries:
        print(f"\nUser: {query}")
        response = chatbot.get_response(query)
        print(f"Bot: {response}")
        print("-"*50) 