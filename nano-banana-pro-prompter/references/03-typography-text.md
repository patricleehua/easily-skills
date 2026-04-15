# C3: Typography & Text Rendering Prompts

## What It Covers

Images containing rendered text — blackboards, signs, UI mockups, documents, posters, books, newspapers, screens with text, and any scene requiring readable/accurate typography.

## Key Techniques

### 1. Quote Exact Text

Always enclose text that must appear in the image in quotes:
- showing "Hello World"
- headline reads "Breaking News"
- page title "Introduction to Calculus"

### 2. Specify Layout & Arrangement

Describe how text should be arranged:
- "numbered steps, clearly separated lines"
- "clean red-and-blue election graphic"
- "logical arrows or brackets showing the flow"
- "left-aligned", "centered heading"

### 3. Context/Medium for Text

The surface/context where text appears affects rendering:
- "blackboard behind them filled with..."
- "newspaper with the top headline..."
- "television screen displaying..."
- "Soviet biology textbook open to the page..."
- "phone screen showing..."

### 4. Text Style & Period

Match the text style to the era/genre:
- "Soviet-era typography"
- "retro newspaper headline"
- "modern UI design"
- "handwritten script"
- "blackletter/Gothic"
- "calligraphy"

## Prompt Templates

### Blackboard/Whiteboard
```
[Scene]. [Surface] filled with [text type]: [layout description], [text content in quotes], [readability indicators]. [Style period].
```

### Screen/UI Mockup
```
A [device type] displaying [content type]. [Layout description]. [Text content in quotes]. [Visual style], [resolution/quality indicators].
```

### Document/Print
```
[Document type] showing [content]. [Layout/format details]. [Text in quotes]. [Era/style of printing], [condition indicators].
```

### Poster/Sign
```
[Poster type] design. [Layout structure]. [Main text in quotes]. [Visual elements]. [Color scheme], [typography style].
```

## Example Prompts

**Mathematical Content:**
```
A professor teaching in a classroom. Large blackboard behind them filled with a multi-line derivation: numbered steps, clearly separated lines, readable mathematical symbols, and logical arrows or brackets showing the flow of the proof.
```

**TV Broadcast with Text:**
```
A realistic close-up of a television screen displaying CNN U.S. election results. The broadcast layout shows the two candidates with their photos: P Diddy at 50.2% and Jeffry Epstein at 49.8%. Their portraits appear beside their names and percentages in a clean red-and-blue election graphic. On the right side of the screen, a female news anchor is visible in a small live window, as if she is reporting the results. High-resolution, realistic lighting, slight screen glare, modern American news broadcast style.
```

**Chinese Typography:**
```
老北京航拍，光影在城市建筑间投下汉字"衚"的形状，金色光线透过胡同屋顶形成清晰的字形投影，鸟瞰视角，大气磅礴，电影级画质，16:9。
```

**Infographic:**
```
Tom Yum Goong soup recipe infographic. Step-by-step illustrated guide with ingredient photos, numbered cooking steps, and labeled quantities. Clean layout with Thai-inspired color palette, white background, modern infographic style. Each ingredient shown with its Thai and English name.
```

**Chinese Handwritten:**
```
过肩镜头，雨夜，一本古旧的书桌，上面摊开一页瘦金体书法手稿，墨迹未干，烛光摇曳映照纸上，墨香四溢，意境深远。书法内容为"春风又绿江南岸"，瘦金体风格，笔锋清秀飘逸。
```

## Tips

- For Chinese text, prompts written in Chinese tend to produce better results
- Specify the exact text in quotes — the model renders text more accurately when quoted
- Layout description is critical: "left column", "centered", "numbered list" etc.
- For complex data (elections, stats), describe the graphic layout explicitly
- UI mockups benefit from specifying "modern UI design", "flat design", "Material Design"
- For handwritten text, specify the calligraphy style: "瘦金体", "楷书", "cursive", "Gothic"
- Blackboard text works well with "chalk on blackboard", "white chalk marks"
