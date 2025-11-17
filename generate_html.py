import os
import re

# Define a unified template that covers common elements from all types
UNIFIED_TEMPLATE = """
<p style="text-align: center;"><span style="background-color: #800000; color: #ffffff;">&nbsp; {warning_text} &nbsp; <br /></span></p>
<p style="text-align: center;"><span style="color: #ff0000;"><strong>{emphasis_text}</strong></span></p>
<p style="text-align: center;"><img src="{image_url}" alt="{image_alt}" width="500" height="700" /></p>
<p style="text-align: center;"><span style="color: #000080;">
{image_description}
</span></p>
<hr id="system-readmore" />
<p style="text-align: justify;"><span style="color: #ff0000;"><strong>خلاصه داستان:&nbsp;</strong></span>{short_summary}</p>
<p style="text-align: justify;">{long_description}</p>
<p>&nbsp;</p>
<p style="text-align: center;">{download_link}</p>
"""

def sanitize_filename(filename):
    """
    Remove or replace invalid characters in a filename.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    sanitized = sanitized.replace(" ", "_")  # Replace spaces with underscores
    return sanitized

def generate_html(title, short_summary, image_url, image_alt, image_description, long_description="", warning_text="", emphasis_text="", video_url="", additional_links="", output_dir="output"):
    # Prepare the download link section
    if video_url:
        download_link = f'<a href="{video_url}"><img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" /></a>'
    else:
        download_link = '<img src="images/52/KEY/00-ftp.png" alt="00 ftp" width="130" height="30" />'
    
    # If additional links are provided (e.g., for Iranian series), append them
    if additional_links:
        download_link += f' &nbsp; &nbsp; &nbsp; {additional_links}'

    # Replace placeholders with actual values, handling optional fields
    html_content = UNIFIED_TEMPLATE.format(
        warning_text=warning_text or "",  # Optional warning (e.g., for Iranian series)
        emphasis_text=emphasis_text or "",  # Optional emphasis (e.g., "قسمت آخر اضافه شد" or documentary note)
        image_url=image_url,
        image_alt=image_alt,
        image_description=image_description,
        short_summary=short_summary,
        long_description=long_description or "",  # Optional long description (actors, about, etc.)
        download_link=download_link
    )

    # Sanitize the title to create a valid filename
    sanitized_title = sanitize_filename(title)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f"{sanitized_title}.html")

    # Write the generated HTML to a file
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML file '{output_filename}' has been generated successfully.")

def main():
    while True:
        # Get user inputs for the unified model
        title = input("Enter the title: ")
        warning_text = input("Enter the optional warning text (e.g., site access note, press Enter to skip): ")
        emphasis_text = input("Enter the optional emphasis text (e.g., 'قسمت آخر اضافه شد', press Enter to skip): ")
        short_summary = input("Enter the short summary (خلاصه داستان کوتاه): ")
        image_url = input("Enter the image URL: ")
        image_alt = input("Enter the image alt text (in English): ")
        image_description = input("Enter the image description (genre, year, etc.): ")
        long_description = input("Enter the long description (actors, about, etc., press Enter to skip): ")
        video_url = input("Enter the video URL (for direct link, press Enter to skip): ")
        additional_links = input("Enter additional links HTML (e.g., '<a href=\"...\"><img ... /></a>', press Enter to skip): ")

        # Generate the HTML file
        generate_html(title,warning_text, emphasis_text, short_summary, image_url, image_alt, image_description, long_description, video_url, additional_links)

        # Ask if the user wants to continue
        choice = input("\nDo you want to generate another file? (y/n): ").lower()
        if choice != "y":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()