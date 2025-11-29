# Bug Fix: First Question Asked Twice

## Problem
The first follow-up question was being asked twice when the user first reported a symptom.

## Root Cause
When starting symptom gathering, the system would:
1. Ask the first question (index 0)
2. BUT not increment the question_index
3. When the user answered, it would still be at index 0
4. So it asked the first question again

## Solution
Added `state['question_index'] = 1` on line 51 when starting symptom gathering. This way:
1. We ask the first question (index 0)
2. We set question_index to 1
3. When the user answers, we get question at index 1 (second question)
4. We increment to 2 for the next question
5. And so on...

## Code Change
```python
if state['stage'] == 'initial' and detected_symptoms:
    # Start symptom gathering
    state['stage'] = 'gathering_symptoms'
    state['symptoms'] = detected_symptoms
    state['symptom_details'][detected_symptoms[0]] = user_message
    state['question_index'] = 1  # NEW: Increment to track that we've asked the first question
    
    # Ask first follow-up question
    follow_up = self._get_follow_up_question(detected_symptoms[0])
```

## Verification
Now the flow works correctly:
- User: "I have a headache"
- Bot: Asks question 0 (first question)
- question_index = 1
- User: [Answer]
- Bot: Asks question 1 (second question)
- question_index = 2
- User: [Answer]
- Bot: Asks question 2 (third question)
- And so on...

## Testing
Test by running the application and reporting a symptom. Verify that each question is asked only once.

