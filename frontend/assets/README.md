# Assets Directory

This directory contains static assets for the BotBlocks application.

## Structure

- `icons/` - Icon files (SVG, PNG)
- Images and graphics used in the application

## Notes

- The application primarily uses emoji icons for a lightweight experience
- Custom images can be added here and referenced in the Streamlit pages
- For production, replace placeholder images with branded assets

## Usage

Reference assets in Streamlit pages:

```python
# Display image
st.image("assets/hero-image.png")

# HTML img tag
st.markdown('<img src="assets/logo.png" width="100"/>', unsafe_allow_html=True)
```

## Recommended Assets

- Logo (SVG/PNG): `logo.png` or `logo.svg`
- Hero image: `hero.png` or `hero.jpg`
- Favicon: `favicon.ico`
- Platform icons: `telegram.svg`, `discord.svg`, `website.svg`
