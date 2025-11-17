import os
import re

# Define templates for different content types
TEMPLATES = {
    "animation": """
    <h3 style="text-align: center;"><span style="color: #ff0000;"><strong>
    {title}
    <br /></strong></span></h3>
    <p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
    <p style="text-align: center;"><span style="color: #000080;">
    {image_description}
    </span></p>
    <p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان: </strong><span style="color: #000000;">
    {summary}
    </span> </span></p>
    <p>&nbsp;</p>
    <p style="text-align: center;"><a><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></a></p>
    """,
    "series": """
    <h3 style="text-align: center;"><span style="color: #ff0000;"><strong>
    {title}
    <br /></strong></span></h3>
    <p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
    <p style="text-align: center;"><span style="color: #000080;">
    {image_description}
    </span></p>
    <p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان: </strong><span style="color: #000000;">
    {summary}
    </span> </span></p>
    <p>&nbsp;</p>
    <p style="text-align: center;"><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></p>
    """,
    "cinema": """
    <h3 style="text-align: center;"><span style="color: #ff0000;"><strong>
    {title}
    <br /></strong></span></h3>
    <p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
    <p style="text-align: center;"><span style="color: #000080;">
    {image_description}
    </span></p>
    <p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان: </strong><span style="color: #000000;">
    {summary}
    </span> </span></p>
    <p>&nbsp;</p>
    <p style="text-align: center;"><a href="{video_url}"><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></a></p>
    """,
    "documentary": """
    <p style="text-align: center;"><span style="color: #ff0000;"><strong>
    {emphasis_text}
    </strong></span></p>
    <p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
    <p style="text-align: center;"><span style="color: #000080;">
    {image_description}
    </span></p>
    <p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان:</strong></span>
    {summary}
    </p>
    <p>&nbsp;</p>
    <p style="text-align: center;"><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></p>
    """
}

# Map first letters to content types
CONTENT_TYPE_MAP = {
    "a": "animation",
    "s": "series",
    "c": "cinema",
    "d": "documentary"
}

def sanitize_filename(filename):
    """
    Remove or replace invalid characters in a filename.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    sanitized = sanitized.replace(" ", "_")  # Replace spaces with underscores
    return sanitized

def generate_html(content_type, title, summary, image_url, image_alt, image_description, emphasis_text=None, video_url=None, output_dir="output"):
    # Ensure the output directory exists
    if content_type not in TEMPLATES:
        raise ValueError(f"Unsupported content type: {content_type}")
    
    # Get the template for the specified content type
    template = TEMPLATES[content_type]

    # Replace placeholders with actual values
    html_content = template.format(
        title=title,
        summary=summary,
        image_url=image_url,
        image_alt=image_alt,
        image_description=image_description,
        emphasis_text=emphasis_text or "",  # Optional emphasis text
        video_url=video_url or ""
    )

    # Sanitize the title to create a valid filename
    sanitized_title = sanitize_filename(title)
    output_dir = os.path.join(output_dir, content_type)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f"{sanitized_title}.html")

    # Write the generated HTML to a file
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML file '{output_filename}' has been generated successfully.")

def main():
    while True:
        # Get user inputs
        print("\nPlease select a content type:")
        print("a: Animation")
        print("s: Series")
        print("c: Cinema")
        print("d: Documentary")
        content_type_key = input("Enter the first letter of the content type (or 'q' to quit): ").lower()

        if content_type_key == "q":
            print("Exiting the program. Goodbye!")
            break

        if content_type_key not in CONTENT_TYPE_MAP:
            print("Invalid content type. Please try again.")
            continue

        content_type = CONTENT_TYPE_MAP[content_type_key]
        title = input("Enter the title: ")
        summary = input("Enter the summary: ")
        image_url = input("Enter the image URL: ")
        image_alt = input("Enter the image alt text (in English): ")
        image_description = input("Enter the image description (genre, year, etc.): ")

        emphasis_text = None
        if content_type == "documentary":
            emphasis_text = input("Enter the optional emphasis text (press Enter to skip): ")

        video_url = None
        if content_type == "cinema":
            video_url = input("Enter the video URL (optional): ")

        # Generate the HTML file
        generate_html(content_type, title, summary, image_url, image_alt, image_description, emphasis_text, video_url)

        # Ask if the user wants to continue
        choice = input("\nDo you want to generate another file? (y/n): ").lower()
        if choice != "y":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()