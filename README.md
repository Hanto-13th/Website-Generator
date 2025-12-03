# Static Site Generator

**A Python project that automatically converts Markdown text into static HTML pages and generate to deploy website**
**The result is customisable changing the templates files (HTML and CSS)**

## ⚠️ Important Notes

⚠️ Some scripts (like main.sh or build.sh) are intended only for local testing.

⚠️ For best results, make sure your Markdown files are properly structured.
**Actually the Markdown syntax accepted:**
- The header (# ) and multiples (1-6 '#')
- Bold text (**)
- Italic text (_)
- Quote (>)
- Unordered list (- )
- Ordered list (i. ) where i is a number begins at 1. and incremented each time
- Code text (`) where the text start and end with
- Image `![image]` follows with the path of your image between parentheses `('IMAGE_PATH')`
- Link `[link]` follows with the path of your link between parentheses `('LINK_PATH')`

⚠️ The generator outputs static HTML — any dynamic features must be manually added using JS/CSS.

### ✨ Features

1. Automatically converts Markdown (.md) files into static HTML (.html).

2. Multi-page project support.

3. Customisable HTML templates (header, CSS, etc.).

4. Static assets (CSS/JS/images) are copied into the output folder.

5. Modular and fully extensible structure.

6. Custom URL with basic path management.

#### 🚀 Installation

**Clone the repository:**

`git clone https://github.com/Hanto-13th/Website-Generator.git`
`cd Website-Generator`


**Create a virtual environment:**

`python -m venv .venv`


**Activate it:**

*Windows*

`.venv\Scripts\activate`


*macOS/Linux*

`source .venv/bin/activate`


##### ▶️ Usage

1. Structure your site into the content directory with .md files

2. Add your assets (CSS files, Images)

3. Run build.sh

4. Run main.sh to local preview or deploy the 'docs' directory online

###### 📘 Example Usage

- Portfolio

- Blog

- Curriculum Vitae

🤝 Contributing

Contributions are welcome!
Feel free to open an issue or submit a pull request.

👤 Author

Hanto-13th – no professional email yet.

📝 License

This project is licensed under the MIT License.
