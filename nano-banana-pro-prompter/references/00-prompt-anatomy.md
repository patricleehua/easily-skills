# NanoBananaPro Prompt Anatomy

## Core Structure

A well-crafted NanoBananaPro prompt follows this layered structure:

```
[Scene/Subject] + [Details/Spatial] + [Style/Medium] + [Technical Modifiers] + [Text Requirements]
```

### Layer 1: Scene/Subject (Required)

The primary subject and action. Start with what the image is about.

```
A cozy dining table scene.
```
```
An animated illustration of a party of five adventurers navigating a cave system.
```
```
A realistic close-up of a television screen displaying CNN U.S. election results.
```

### Layer 2: Details & Spatial (Important)

Add specific visual details, positions, and spatial relationships.

Key techniques:
- **Position**: "On the wall", "on the right side", "in the middle distance", "in the far background"
- **Relative**: "standing symmetrically", "next to her left", "behind them"
- **Count**: exact numbers when precision matters ("five adventurers", "twin axes")
- **Physical properties**: materials, textures, colors, states

```
On the wall, a clock showing exactly 11:15 with correct tick marks.
A crystal wine glass on the table is filled exactly to the rim with liquid.
```

### Layer 3: Style/Medium (Recommended)

Specify the visual medium or style.

Common styles:
- Photography: "35mm film photograph", "iPhone selfie", "CCTV footage", "Polaroid", "Product photography"
- Film: "Frame from a 1953 motion picture in technicolor", "Cinematic"
- Illustration: "Animated illustration", "Comic-book", "Watercolor"
- 3D: "3D character model", "Realistic 1/7 scale figure"
- Design: "Infographic", "Poster design", "UI design"

### Layer 4: Technical Modifiers (Optional but powerful)

Camera and lighting:
- Lens: "50mm lens look", "wide-angle"
- Film stock: "35mm film", "Kodak Portra 400", "visible film grain"
- Lighting: "Soft daylight", "golden hour", "natural lighting", "studio lighting"
- Color: "muted color palette", "bold, saturated colors", "desaturated"
- Atmosphere: "somber and powerful atmosphere", "cozy", "dreamy"

Aspect ratio:
- `16:9` — cinematic widescreen
- `2:3` — portrait orientation
- `1:1` — square
- Can also describe in text: "vertical orientation", "wide panoramic"

### Layer 5: Text Requirements (For C3 Typography)

When text must appear in the image:
- Quote exact text: showing exactly "Hello World"
- Specify layout: "clean red-and-blue election graphic", "numbered steps, clearly separated lines"
- Style the text context: "Soviet biology textbook", "retro newspaper headline"

## Prompt Length Guide

NanoBananaPro handles both short and long prompts effectively:

**Short (1 sentence):** Best for surreal/creative concepts where the model fills in details.
```
A motorbike made of sharks
```

**Medium (2-3 sentences):** Good for most use cases with some specificity.
```
cctv footage, UK. a man in the street wearing gigantic oversized sneakers. talking to a police officer.
```

**Long (4+ sentences):** Essential for multi-character scenes or precise requirements.
```
an animated illustration of a party of five adventurers navigating a cave system. In the middle, the tall, old guide stands. He is dressed in navy blue wizard robes. [continues with detailed character descriptions...]
```

## Common Patterns

### Negative Construction (for precision)
```
...filled exactly to the rim with liquid—no spill, realistic meniscus
```

### Reference Image Placeholder (for C9 Image Editing)
```
Combine multiple images ([Image1], [Image2], [Image3]) into a single cohesive image.
```

### Period/Era Styling
```
1940's styling. Frame from a 1953 motion picture in technicolor.
```
```
90年代情书风格
```

### Quality Reinforcement
```
High-resolution, realistic lighting, slight screen glare
```
```
Photorealistic, high-resolution, seamless integration
```
