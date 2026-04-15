# C9: Image Editing & Compositing Prompts

## What It Covers

All prompts that use reference images for editing — compositing, style transfer, object manipulation, background replacement, outpainting, color grading, and image-to-image transformations.

## Key Techniques

### 1. Reference Image Placeholders

Use `[Image1]`, `[Image2]`, `[Image3]` notation to reference input images:
```
Combine multiple images ([Image1], [Image2], [Image3]) into a single cohesive image.
```

### 2. Editing Operation Categories

**Compositing** — Merge multiple images:
```
Combine multiple images ([Image1], [Image2], [Image3]) into a single cohesive image. Keep all key subjects recognizable and maintain their proportions and details. Blend the images naturally with consistent lighting, shadows, perspective, and style. Photorealistic, high-resolution, seamless integration.
```

**Style Transfer** — Apply style from one image to another:
```
Apply the artistic style of [Image1] to the content and composition of [Image2]. Preserve the subject matter and layout of [Image2] while adopting the color palette, brushwork, and visual mood of [Image1].
```

**Object Manipulation** — Add, remove, or modify elements:
```
[Add/Remove/Replace] [element] in [Image1]. [Description of change]. Maintain [preserved elements]. [Quality directives].
```

**Background Replacement** — Change the scene:
```
Replace the background of [Image1] with [new background description]. Keep the subject [description of preservation]. Match [lighting/perspective/color] to the new environment. Seamless blending.
```

**Outpainting** — Extend the image:
```
Extend [Image1] outward in [direction(s)]. Continue the [scene/texture/lighting] naturally. [Additional context for extended area]. Consistent style and quality with the original.
```

### 3. Preservation Directives

Always specify what must be preserved:
- "maintain their proportions and details"
- "Preserve the subject matter and layout"
- "Keep the subject's identity and features"
- "consistent lighting, shadows, perspective, and style"

### 4. Quality Consistency

Bridge the gap between original and edited:
- "seamless integration"
- "consistent style and quality with the original"
- "natural blending at boundaries"
- "matching color temperature and lighting direction"

## Prompt Templates

### Composite Multiple Images
```
Combine [Image1] and [Image2] into a single cohesive image. [Subject from Image1] [action/relation] [subject from Image2]. [Blending instructions]. Consistent [lighting/perspective/style]. Photorealistic, seamless integration.
```

### Style Transfer
```
Redraw [Image1] in the style of [Image2]. [What to preserve from Image1]. [What to adopt from Image2]. [Quality/mood directives].
```

### Outfit/Attribute Swap
```
[Subject from Image1] wearing [clothing/attribute from Image2]. [Fit/body type adjustments]. [Background/lighting]. Maintain subject's identity and features.
```

### Object Removal/Addition
```
[Add/Remove] [element] [to/from] [Image1]. [Description of modification]. [What to preserve]. [Lighting/perspective matching]. High-resolution result.
```

### Outpainting/Extension
```
Extend [Image1] [direction] to create a [aspect ratio] composition. [Description of new area]. Continue the [mood/lighting/style]. Seamless transition at the boundary.
```

### Color Grading
```
Apply the color grading and palette from [Image1] to [Image2]. [Specific adjustments: warmth, contrast, saturation]. [Mood to achieve]. Preserve the content and composition of [Image2].
```

## Example Prompts

**Multi-Image Composite:**
```
Combine multiple images ([Image1], [Image2], [Image3]) into a single cohesive image. Keep all key subjects recognizable and maintain their proportions and details. Blend the images naturally with consistent lighting, shadows, perspective, and style. Photorealistic, high-resolution, seamless integration.
```

**Style Transfer (Ghibli):**
```
Redraw the scene from [Image1] in Studio Ghibli anime style. Keep the composition, characters, and setting identical. Use Ghibli's signature watercolor backgrounds, soft pastel tones, and warm lighting. Maintain the emotional tone of the original.
```

**Pose Transfer:**
```
[Person from Image1] in the same pose as [Person from Image2]. Keep the identity, clothing, and features of [Image1]. Match the body position, camera angle, and perspective of [Image2]. Realistic lighting and proportions.
```

**Background Replacement:**
```
Replace the background of [Image1] with [new scene description]. Keep the subject exactly as-is, preserving their appearance, clothing, and pose. Match the lighting direction and color temperature to the new environment. Seamless edge blending.
```

## Tips

- Always use `[Image1]`, `[Image2]` notation consistently
- Preservation instructions are critical — without them, the model may alter too much
- "Seamless integration" and "natural blending" help avoid obvious compositing artifacts
- For style transfer, describe the style in both visual and emotional terms
- Reference images can be described by their content: "the portrait photo" vs "the painting"
- For outpainting, describe the extended area's content — don't leave it vague
- Multiple editing operations can be chained, but clarity decreases with complexity
