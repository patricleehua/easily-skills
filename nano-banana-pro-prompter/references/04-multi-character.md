# C4: Multi Character Prompts

## What It Covers

Scenes with multiple distinct characters, each with unique appearances, poses, and positions. Group photos, fantasy parties, sports teams, and any scene with 2+ interacting characters.

## Key Techniques

### 1. Describe Characters Separately

Describe each character as a complete unit:
- Position relative to others
- Physical appearance (build, clothing, features)
- Action/pose
- Key props/items

### 2. Use Spatial Anchors

Establish spatial relationships:
- "In the middle" — center anchor
- "On his right" — relative positioning
- "On the left of the guide" — directional
- "Next to her left" — sequential
- "standing symmetrically" — composition

### 3. Character Description Order

Follow this order for each character:
```
Position → Build/Height → Clothing → Distinctive Features → Action → Props
```

### 4. Balance Detail Across Characters

Give roughly equal detail to each character to ensure they all render well.

## Prompt Templates

### Fantasy/Adventure Party
```
[Scene setting]. In the middle, [Character 1 anchor]: [appearance], [clothing], [features]. [Position], [Character 2]: [appearance], [clothing], [features], [action], [props]. [Position], [Character 3]: [appearance], [clothing], [action]. Continue for each character. [Overall mood/lighting].
```

### Group Interaction
```
[Scene context]. [Character A] [action] toward [Character B]. [Character A appearance]. [Character B appearance]. [Other characters in background/foreground]. [Overall composition].
```

### Sports/Action
```
[Sports scene]. [Player 1] [action] against [Player 2]. [Player 1 team/uniform]. [Player 2 team/uniform]. [Setting/stadium details]. [Action moment description]. [Camera angle], [lighting].
```

## Example Prompts

**Detailed Fantasy Party (5 characters):**
```
an animated illustration of a party of five adventurers navigating a cave system. In the middle, the tall, old guide stands. He is dressed in navy blue wizard robes. He has a silver goatee and a wise smile on his face. He holds a brown walking stick. He is carrying a heavy load of packs. A grimoire floats next to him, creating a luminescent light to guide the way. On his right, stands the towering Berserker. The berserker is wearing fur armor. He has a sculpted, muscular and tall build. His muscles are covered in storm lightning runes that flicker and crack. He is carrying twin axes, one in his left hand, and another in his axe holster on his hip. He has a large bastardsword on his back. He is gnawing on a huge piece of meat which he holds with his right hand. On the right of the berserker stands the pretty, fair-skinned healer. She is short and cute, wearing pure white priestess robes with golden trim. She has blonde hair and she is actually levitating a bit off the ground, with an aura around her. On the left of the guide stands a mischievous, redhead archer with a crafty smile on her face. She is drawing her bow. She has a number of arrows on her back and bombs strapped to her leather armor. She is slender and of average height. Next to her left stands the bald monk with five shaolin marks on his head. He wears orange monk robes and has a lean-muscular build. He is wearing sandals. He is carrying daoist beads and holding his hands close together in prayer.
```

**Humorous Interaction:**
```
A grizzly bear holding a picture with a meme of a grizzly bear in the forest, in front of a real hiker.
```

**Animals with Personality:**
```
A duck, a chicken and a parrot riding a scooter together. The duck is driving, wearing sunglasses. The chicken sits behind holding onto the duck, looking nervous. The parrot perches on the handlebars, wings spread wide.
```

## Tips

- Start with a center/anchor character, then describe others relative to them
- More characters = longer prompts. Don't be afraid to write 200+ words
- Give each character a distinctive visual trait (color, build, accessory)
- Specify actions clearly to avoid ambiguity
- For 5+ characters, use spatial sequencing (left to right, or center outward)
- Balance the description — if one character has 3 sentences, others should too
- Animals as characters work well (duck on scooter, whippet on moped)
