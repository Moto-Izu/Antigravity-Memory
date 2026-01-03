---
description: Generates a daily 8-panel manga summary of the day's work using the generated_image tool with character consistency reference.
trigger: manual
slug: manga
---

# Daily Manga Generation Workflow

This workflow generates a high-quality 8-panel manga summarizing the latest daily log, ensuring character consistency for "Seira" and the developer.

## Step 1: Analyze Context

1.  **Identify Date**: Determine the date of the latest log (e.g., today or the date of the latest file in `logs/YYYY/MM/`).
2.  **Read Log**: Read the content of that log file to understand the key events.
3.  **Draft Story**: Create an 8-panel storyboard.
    *   **Characters**:
        *   **Developer**: Male, glasses, hoodie, short hair (Reference: `manga/2026/2026-01-01.png`).
        *   **Seira**:
            *   **Before upgrade**: Cute floating round robot.
            *   **After upgrade**: Cute anime girl (light blue hair, digital futuristic dress).
    *   **Style**: Full color, bright, anime style.

## Step 2: Generate Image

Use the `generate_image` tool (NOT the basic text-to-image tool if it precludes reference images) to generate the manga.

*   **Tool**: `generate_image`
*   **Reference Image**: MUST include `ZG_PROJECT/<project_name>/manga/2026/2026-01-01.png` (Absolute path) in `ImagePaths` to ensure character consistency.
*   **Prompt**:
    *   Format: "A high-quality 8-panel manga page (vertical layout) with JAPANESE TEXT."
    *   Details: Describe the 8 panels based on the drafted story.
    *   Style constraint: "Match the style of the provided reference image exactly. Full color."

## Step 3: Save and Commit

1.  **Save**: Save the image to `manga/YYYY/YYYY-MM-DD.png`.
2.  **Commit**:
    ```bash
    git add manga/YYYY/YYYY-MM-DD.png
    git commit -m "docs: add daily manga for YYYY-MM-DD"
    git push origin main
    ```

## Step 4: Notify

Notify the user that the manga is ready and open the file.
