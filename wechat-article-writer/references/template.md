# WeChat Article Reusable Template

This template defines the complete article structure, layout specifications, and quality checklist.

---

## Article Structure Template

### Part 1: Opening (Golden 30 Seconds)

```
[IMG:opening] -- Scene-setting image (personal photo, product screenshot, or context image)

[Scene Entry]
One concrete personal experience or scenario. 2-3 sentences max.
Must be specific: time, place, tool, situation.

[Pain Point]
Directly state the problem readers likely face.
One sentence. Sharp.

[Value Preview]
Tell readers exactly what they will gain from this article.
Format: "Today I will share..." or "This article will help you..."

[Emotional Hook]
One line that triggers "same here" resonance.
Can be a rhetorical question or a bold statement.
```

**Word count target**: 80-120 words

---

### Part 2: Body (Three-Act Narrative)

#### Act 1 -- Exploration Process

```
[What I Did]
Specific actions taken. Use first person.
Include timestamps or duration for credibility.

[IMG:process] -- Screenshot of initial setup or first attempt

[What Went Wrong]
Document real setbacks, errors, failed attempts.
Self-deprecating tone is encouraged (Kazik style).
Be specific: error messages, unexpected results, time wasted.

[How I Fixed It]
Step-by-step resolution.
Use numbered list for clarity.
Include configuration details or code snippets where relevant.
```

**Word count target**: 300-500 words

#### Act 2 -- Core Findings

```
[Key Insight]
1-2 core takeaways presented as bold standalone statements.
Each insight gets its own paragraph.

[IMG:process] -- Demonstration screenshot or diagram

[Detailed Walkthrough]
Expand on each insight with:
- What it means (1 sentence)
- Why it matters (1-2 sentences)
- How to apply it (concrete steps or examples)

[Results / Data]
Present outcomes using:
- Before/after comparison tables
- Performance metrics (with numbers)
- Visual demonstrations

[IMG:result] -- Result visualization or comparison chart
```

**Word count target**: 400-600 words

#### Act 3 -- Elevated Thinking

```
[Industry Significance]
Zoom out to bigger picture.
Connect personal finding to industry trend or broader implication.

[Personal Reflection]
Share growth insight or mindset shift.
Vulnerable and honest tone.

[Actionable Advice]
3-5 bullet points of concrete next steps.
Each must be immediately executable by the reader.
```

**Word count target**: 200-300 words

---

### Part 3: Closing (Loop Design)

```
[One-Line Summary]
Single sentence that captures the entire article's core value.

[Call to Action]
Specific next step for the reader.
Examples: "Try this tool today", "Set aside 30 minutes this weekend to..."

[Discussion Prompt]
One open question for the comments section.
Must be genuine, not generic.

[Teaser]
One-line hint about the next article's topic.
Creates anticipation without over-promising.
```

**Word count target**: 80-120 words

---

## Typography & Layout Specifications

### Font Style

| Element | Specification |
|---|---|
| Article Title | 18-20px, bold, primary brand color |
| Section Headers | 16-17px, bold, slightly lighter than title color |
| Body Text | 16px, regular weight, line-height 1.8, color #333333 |
| Emphasized Text | Bold or color-highlighted (brand accent color) |
| Code Blocks | Monospace font, #f5f5f5 background, 1px #ddd border, rounded corners |
| Blockquotes | Left border in brand color, lighter background |

### Paragraph Layout

- **Paragraph length**: 2-3 lines maximum. Never exceed 4 lines.
- **Spacing**: One blank line between paragraphs.
- **Key statements**: Extract to standalone paragraphs, bold the core phrase.
- **Lists**: Use unordered (bullet) for features/tips, ordered (numbered) for steps.
- **Tables**: Use for comparisons, specifications, or structured data.

### Color Palette (Recommendation)

| Token | Hex | Usage |
|---|---|---|
| Primary | #1a1a2e | Titles, key emphasis |
| Accent | #16213e | Section headers |
| Body | #333333 | Main text |
| Light BG | #f8f9fa | Code blocks, callouts |
| Highlight | #e94560 | Critical emphasis, warnings |

---

## Image Placement Strategy

| Position | Marker | Type | Frequency |
|---|---|---|---|
| Article start | `[IMG:opening]` | Scene-setting photo or product shot | Exactly 1 |
| Throughout body | `[IMG:process]` | Screenshots, flowcharts, UI captures | Every ~300 words |
| Results section | `[IMG:result]` | Before/after, charts, metrics | 1-2 per article |
| Article end | `[IMG:closing]` | Summary infographic or personal photo | 0-1 |

### Image Requirements
- Width: Full article width (no half-width images)
- Alt text: Descriptive caption below each image
- Style: Consistent border radius, no heavy filters
- Screenshots: Must show relevant UI elements with optional annotations

---

## Four-Layer Quality Checklist

### L1 -- Basic Standards (Must Pass)

- [ ] No AI-flag words in Chinese: , , , , 
- [ ] Correct punctuation (no triple exclamation marks, no missing periods)
- [ ] No textbook-style openings ("With the development of..." / "In recent years...")
- [ ] Zero typos
- [ ] All links and references are real, not fabricated

### L2 -- Style Consistency (Must Pass)

- [ ] Opening starts from a concrete personal scenario
- [ ] Long and short sentences alternate with rhythm
- [ ] At least one self-deprecating or humorous moment
- [ ] Conversational tone level matches selected style (Kazik: high / Samuel: moderate)
- [ ] Paragraphs are short (2-3 lines), no walls of text

### L3 -- Content Quality (Must Pass)

- [ ] Every claim has specific supporting evidence
- [ ] Knowledge is embedded in narrative, not delivered as lecture
- [ ] Contains at least one elevated industry-level or cultural insight
- [ ] Opposing viewpoints or limitations are acknowledged
- [ ] Actionable takeaways are concrete, not vague

### L4 -- Live-Person Feel Audit (Final Gate)

- [ ] Reads like a real person talking to a friend
- [ ] Has emotional warmth, not cold information delivery
- [ ] Reader can sense the author's personality and emotion
- [ ] Triggers "I want to try this too" impulse
- [ ] No section feels like it was generated by a template

---

## Quick Creation Workflow

```
Step 1: Topic Selection (HKR Check)
  H: Would you click this title?
  K: Will the reader learn something new?
  R: Does it resonate emotionally?
  Pass all 3 -> proceed. Fail any -> rework topic.

Step 2: Outline (Hero's Journey)
  - Start: Problem / Curiosity
  - Journey: Exploration + Setbacks
  - Turn: Key discovery / Breakthrough
  - End: "Wow" result
  - Return: Value for the reader

Step 3: Draft (AI-Human Collaboration)
  AI handles: Evidence gathering, analogies, angle expansion, background research
  Human handles: First-hand observations, core creativity, emotional expression, empathy

Step 4: Polish (Loop Design)
  - Callback: Opening hook must echo in the closing
  - Core image: Thread a consistent metaphor throughout
  - Narrative arc: Must form a complete loop

Step 5: Self-Check (Four-Layer Audit)
  Run through all 4 layers before publishing.
  Fix any failed items before release.
```
