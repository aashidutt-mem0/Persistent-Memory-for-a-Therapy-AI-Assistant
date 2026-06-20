"""Pre-written therapy sessions and deterministic extracted memories."""

PATIENT_ID = "alex-rivera"
THERAPIST = "Dr. Maya Chen"

SESSIONS = {
    3: {
        "title": "Session 3 - Sunday panic, sertraline side effects, CBT grounding",
        "date": "2026-05-04",
        "summary": "Alex describes Sunday-night panic attacks, sertraline GI issues, and learns CBT grounding.",
        "transcript": """Dr. Chen: Last week you mentioned the attacks felt less random than before. Did you notice any pattern?

Alex: It is almost always Sunday evening. Around 7 or 8 PM I start thinking about Monday, my chest tightens, and then I cannot sleep. Monday morning is when I am most afraid of another panic attack.

Dr. Chen: That sounds like anticipatory anxiety building into panic. How many attacks are you averaging right now?

Alex: About three a week. I would really like to get below one a week.

Dr. Chen: Let's start tracking the Sunday-night pattern. How did the medication trial go?

Alex: I stopped sertraline in week three. It was 50 milligrams, but the nausea and diarrhea were too much. It did not feel neurological or anything, mostly GI.

Dr. Chen: Thank you for being specific. Any allergies your psychiatrist should know about?

Alex: Penicillin. I always forget to mention that.

Dr. Chen: Today I want to introduce a CBT grounding skill. When you feel the panic ramping up, name five things you see, four you can touch, three you hear, two you smell, and one you taste. We'll test whether it changes the intensity.""",
        "facts": [
            {
                "id": "dx-history",
                "category": "Diagnosis & History",
                "memory": "Alex is being treated for panic disorder and generalized anxiety disorder.",
                "display": "Panic disorder and generalized anxiety disorder",
                "keywords": ["panic", "gad", "diagnosis", "history"],
            },
            {
                "id": "provider",
                "category": "Diagnosis & History",
                "memory": "Alex is in ongoing therapy with Dr. Maya Chen.",
                "display": "3 therapy sessions with Dr. Chen (ongoing)",
                "keywords": ["therapy", "provider", "dr chen", "history"],
            },
            {
                "id": "sunday-trigger",
                "category": "Triggers & Patterns",
                "memory": "Panic attacks correlate with Sunday evenings and anticipatory anxiety about Monday.",
                "display": "Panic attacks correlate with Sunday evenings",
                "keywords": ["sunday", "trigger", "panic", "monday", "anticipatory"],
            },
            {
                "id": "sertraline-gi",
                "category": "Medications",
                "memory": "Sertraline 50mg was stopped in week 3 because of GI side effects: nausea and diarrhea.",
                "display": "Sertraline 50mg stopped week 3 - GI side effects (nausea, diarrhea)",
                "keywords": ["sertraline", "medication", "gi", "nausea", "diarrhea"],
            },
            {
                "id": "grounding-introduced",
                "category": "Coping Strategies",
                "memory": "CBT 5-4-3-2-1 grounding technique was introduced in session 3.",
                "display": "CBT grounding technique introduced",
                "keywords": ["cbt", "grounding", "coping"],
            },
            {
                "id": "penicillin-allergy",
                "category": "Allergies",
                "memory": "Alex has a penicillin allergy.",
                "display": "Penicillin allergy",
                "keywords": ["penicillin", "allergy"],
            },
        ],
    },
    7: {
        "title": "Session 7 - PMR tried, grounding works only for mild episodes",
        "date": "2026-06-01",
        "summary": "Alex reports that progressive muscle relaxation was unhelpful, but journaling continues.",
        "transcript": """Dr. Chen: You were going to test progressive muscle relaxation for two weeks. What happened?

Alex: I tried it. It made me focus too much on my body, and that made the panic feel closer. I do not want to keep using PMR.

Dr. Chen: Good data. We can retire that strategy. How about grounding?

Alex: The 5-4-3-2-1 thing helps if the anxiety is mild. If it is a full attack, it is not enough. Journaling helps me catch the Sunday spiral earlier, though.

Dr. Chen: How many panic attacks this week?

Alex: Down to about 2.4 per week if I average the last month. Better than three, but not close to below one.

Dr. Chen: For psychiatry, it will help to know what works, what does not, and where the goal still stands.""",
        "facts": [
            {
                "id": "pmr-abandoned",
                "category": "Coping Strategies",
                "memory": "Progressive muscle relaxation was tried in session 7 and Alex found it unhelpful, so it was abandoned.",
                "display": "PMR tried in session 7, patient found it unhelpful",
                "keywords": ["pmr", "progressive muscle relaxation", "coping", "unhelpful"],
            },
            {
                "id": "grounding-severity",
                "category": "Coping Strategies",
                "memory": "CBT grounding is effective for mild anxiety episodes but less effective for severe panic attacks.",
                "display": "CBT grounding is effective for mild episodes, less for severe attacks",
                "keywords": ["grounding", "cbt", "mild", "severe", "panic"],
            },
            {
                "id": "journaling",
                "category": "Coping Strategies",
                "memory": "Alex journals consistently and uses it to catch the Sunday anxiety spiral earlier.",
                "display": "Journaling: patient engages consistently",
                "keywords": ["journaling", "coping", "sunday"],
            },
            {
                "id": "treatment-goal",
                "category": "Treatment Goals",
                "memory": "Treatment goal is to reduce panic attacks from 3 per week to less than 1 per week; current rate is about 2.4 per week.",
                "display": "Reduce panic attacks from 3/wk to <1/wk (current: 2.4/wk)",
                "keywords": ["goal", "panic", "frequency", "2.4"],
            },
        ],
    },
    11: {
        "title": "Session 11 - Box breathing helps sleep anxiety, sleep is declining",
        "date": "2026-06-15",
        "summary": "Alex finds box breathing useful before sleep, but sleep continues to decline.",
        "transcript": """Dr. Chen: Last time we added box breathing before bed. Four counts in, hold, out, hold. How did that land?

Alex: It helps before sleep, especially Sunday. It gives me something concrete to do. But sleep is still getting worse. I averaged 5.2 hours this week, and it has been declining for about three weeks.

Dr. Chen: What happens after the poor sleep?

Alex: Monday is rough. Sunday evening anxiety turns into bad sleep, and then Monday panic feels more likely.

Dr. Chen: When you meet the psychiatrist, how do you want them to communicate with you?

Alex: Direct is better. I do not need it sugarcoated, just clear options and side effects. Also I am not taking any psychiatric meds right now since stopping sertraline.""",
        "facts": [
            {
                "id": "box-breathing",
                "category": "Coping Strategies",
                "memory": "Box breathing is helpful for Alex's pre-sleep anxiety, especially on Sundays.",
                "display": "Box breathing: helpful for pre-sleep anxiety",
                "keywords": ["box breathing", "sleep", "sunday", "coping"],
            },
            {
                "id": "sleep-decline",
                "category": "Sleep",
                "memory": "Alex is averaging 5.2 hours of sleep per night, declining over the last 3 weeks.",
                "display": "Averaging 5.2 hours/night, declining over 3 weeks",
                "keywords": ["sleep", "5.2", "declining"],
            },
            {
                "id": "sunday-sleep-monday",
                "category": "Triggers & Patterns",
                "memory": "Sunday evening anxiety contributes to poor sleep, which increases Monday panic risk.",
                "display": "Sunday evening -> anticipatory anxiety -> poor sleep -> Monday panic",
                "keywords": ["sunday", "sleep", "monday", "panic", "trigger"],
            },
            {
                "id": "direct-style",
                "category": "Preferences",
                "memory": "Alex responds better to a direct communication style with clear options and side effects.",
                "display": "Responds better to direct communication style",
                "keywords": ["preference", "direct", "communication"],
            },
        ],
    },
}


REFERRAL_LETTER = """Dear Psychiatry Team,

I am referring Alex Rivera for medication evaluation. Alex is being treated for panic disorder and generalized anxiety disorder. Alex tried sertraline and discontinued it due to side effects. Alex is currently using CBT techniques with partial success.

Sincerely,
Dr. Maya Chen"""


MISSED_DETAILS = [
    "Which side effects: GI symptoms, not neurological symptoms",
    "Which coping strategies work for which severity",
    "Sleep trend: 5.2h average and declining",
    "Sunday night trigger pattern",
    "Treatment goal: 3/wk -> <1/wk, currently 2.4/wk",
    "PMR tried and abandoned",
]
