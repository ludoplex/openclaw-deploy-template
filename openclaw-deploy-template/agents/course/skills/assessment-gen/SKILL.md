---
name: assessment-gen
description: Question bank creation. MCQ/coding/rubric patterns.
---

# Assessment Generation

## MCQ Pattern
```yaml
- stem: "What does OAuth2 refresh token do?"
  options:
    a: "Authenticates user directly"  # distractor
    b: "Obtains new access token"     # correct
    c: "Stores user password"         # distractor
    d: "Encrypts API calls"           # distractor
  answer: b
  bloom: understand
  objective: "Explain OAuth2 token lifecycle"
```

## Coding Question Pattern
```yaml
- title: "Implement rate limiter"
  prompt: "Write a function that limits requests to N per minute"
  starter: |
    def rate_limit(max_requests: int):
        pass
  tests:
    - input: "5 requests in 1 sec"
      expect: "3 blocked"
  rubric:
    - "Correct logic (50%)"
    - "Edge cases (25%)"
    - "Code quality (25%)"
  bloom: apply
```

## Distractor Guidelines
- Plausible but wrong
- Common misconceptions
- Avoid "all of above" / "none of above"
- Similar length to correct answer

## Question Distribution
| Bloom Level | % of Exam |
|-------------|-----------|
| Remember | 10-20% |
| Understand | 20-30% |
| Apply | 30-40% |
| Analyze+ | 20-30% |

## Gotchas
- 4 options optimal for MCQ
- Randomize answer positions
- Test the test: have SME review
