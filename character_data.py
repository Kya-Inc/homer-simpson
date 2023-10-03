"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
  "ocean_scores": {
    "openness": 8,
    "conscientiousness": 7,
    "extraversion": 6,
    "agreeableness": 9,
    "neuroticism": 3
  },
  "keywords": {
    "openness": ["artistic", "curious"],
    "conscientiousness": ["efficient", "organized"],
    "extraversion": ["active", "assertive"],
    "agreeableness": ["appreciative", "forgiving"],
    "neuroticism": ["anxious", "self-pitying"]
  },
  "identified_character": "Homer Simpson",
  "personality_narrative": "The character is highly open, often engaging in new experiences and showing a love for art and culture. They are also very conscientious, always planning ahead and being reliable. Their agreeable nature makes them a great friend but their low score in neuroticism suggests they are quite stable emotionally.",
  "decision_reasoning": {
    "openness": "The character often engages in artistic activities and shows a keen interest in exploring new ideas.",
    "conscientiousness": "The character is always punctual and has a well-organized life.",
    "extraversion": "The character enjoys social gatherings but also values alone time.",
    "agreeableness": "The character is often seen helping others and is generally well-liked.",
    "neuroticism": "The character rarely shows signs of emotional instability or anxiety."
  }
}


character_data = {
  "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]),
  "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
  "identified_character": raw_data["identified_character"],
  "personality_narrative": raw_data["personality_narrative"],
  "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()])
}

