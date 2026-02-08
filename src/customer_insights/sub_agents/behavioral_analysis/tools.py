from __future__ import annotations

import random
from typing import Any, Dict, List

from faker import Faker


def generate_synthetic_behavioral_data(
    num_segments: int = 3, seed: int | None = None
) -> List[Dict[str, Any]]:
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    segments = []
    segment_templates = [
        ("value-driven-lunch-buyer", "Lunch buyers seeking value during weekdays."),
        ("late-night-craver", "Late night snackers focused on craveable items."),
        ("family-bundle-planner", "Family buyers preferring bundled meals."),
    ]

    for i in range(num_segments):
        segment_id, description = segment_templates[i % len(segment_templates)]
        segments.append(
            {
                "segment_id": segment_id,
                "segment_description": description,
                "empirical_metrics": {
                    "redemption_rate": f"{round(random.uniform(1.6, 2.8), 1)}x",
                    "lift_estimate": f"{round(random.uniform(8, 22), 1)}%",
                    "segment_size": f"{random.randint(8, 25)}%",
                    "channel_preference": random.choice(
                        ["app", "drive-thru", "delivery", "in-store"]
                    ),
                },
                "behavioral_patterns": [
                    f"Typical visit time: {random.choice(['weekday lunch', 'late night', 'weekend'])}.",
                    f"Average order size: ${random.randint(8, 18)}.",
                    f"Promotion responsiveness: {random.choice(['high', 'medium', 'growing'])}.",
                ],
                "sample_customer": {
                    "name": fake.first_name(),
                    "city": fake.city(),
                },
            }
        )
    return segments
