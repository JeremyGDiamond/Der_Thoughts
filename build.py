import os
import shutil
import sys
import pypandoc
from datetime import datetime
import email.utils  # for RFC 2822 date formatting

# Define paths
POSTS_DIR = "posts"
OUTPUT_DIR = "deploy"
HEADER_FILE = "header.html"
FOOTER_FILE = "footer.html"
POSTS_FILE = os.path.join(OUTPUT_DIR, "posts.html")
RSS_FILE = "rss.xml"

# input args and valdation 
# blog_url, blog_name, rss_des_file
if len(sys.argv) != 4:
    print ('''Error: wrong number of inputs\n   Usage:\n   python build.py blog_url blog_name rss_des_file\n   blog_url: url to deploy to
   blog_name: Name of blog in text\n   rss_des_file: txt file with the description of the blog for the rss feed, use \"nill\" to skip''')
if sys.argv[3] == "nill":
    print("INFO: skipping rss_des_file")

blog_url = sys.argv[1]
blog_name = sys.argv[2]
rss_des_file = sys.argv[3]

print (f"blog_url = {blog_url}")
print (f"blog_name = {blog_name}")
print (f"rss_des_file = {rss_des_file}")

# Make sure the output folders exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load header and footer
with open(HEADER_FILE, "r", encoding="utf-8") as f:
    header_html = f.read()

with open(FOOTER_FILE, "r", encoding="utf-8") as f:
    footer_html = f.read()

posts_html = []
posts_html.append("<main>")
posts_html.append('<div class="posts-list">')

# Store metadata for RSS
rss_items = []

for post_dir in sorted(os.listdir(POSTS_DIR)):
    full_post_dir = os.path.join(POSTS_DIR, post_dir)
    if not os.path.isdir(full_post_dir):
        continue

    # Split directory name: "YYYY,MM,DD:postname"
    if ":" not in post_dir:
        print(f"Skipping {post_dir}: no date prefix found.")
        continue

    delimindex = post_dir.find(":")
    date_part = post_dir[:delimindex]
    post_name = post_dir[delimindex + 1:]
    post_date = date_part.replace(",", "-")  # convert to "YYYY-MM-DD"

    md_path = os.path.join(full_post_dir, "post.md")
    desc_path = os.path.join(full_post_dir, "des.txt")
    img_path = os.path.join(full_post_dir, "thumb.jpg")

    if not os.path.exists(md_path):
        print(f"Skipping {post_dir}: no post.md file found.")
        continue

    print(f"Building post: {post_name}")

    # Convert Markdown → HTML body
    post_html_body = pypandoc.convert_file(md_path, "html", format="md")

    # Output filenames (flat structure)
    html_filename = f"{post_name}.html"
    html_output_path = os.path.join(OUTPUT_DIR, html_filename)
    img_output_path = os.path.join(OUTPUT_DIR, f"{post_name}.jpg")

    # Build full HTML document
    post_html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{post_name.replace('-', ' ').title()} — {blog_name}/title>",
        '<link rel="stylesheet" href="/style.css">',
        "</head>",
        "<body>",
        header_html,
        "<main>",
        post_html_body,
        "</main>",
        footer_html,
        "</body>",
        "</html>",
    ]

    # Write post HTML
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(post_html))

    # Copy thumbnail
    if os.path.exists(img_path):
        shutil.copy(img_path, img_output_path)

    # Load description
    description = ""
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            description = f.read().strip()

    # Add entry to the index
    posts_html.append('<div class="post-card">')

    if os.path.exists(img_path):
        posts_html.append(
            f'<a href="{OUTPUT_DIR}/{html_filename}"><img src="{OUTPUT_DIR}/{os.path.basename(img_output_path)}" alt="{post_name}" class="thumbnail"></a>'
        )

    posts_html.append(f'<h3><a href="{OUTPUT_DIR}/{html_filename}">{post_name.replace("-", " ").title()}</a></h3>')

    if description:
        posts_html.append(f"<p>{description}</p>")

     
    posts_html.append("<h2>|</h2>") # spacing for postcards, use depends on css rules

    posts_html.append("</div>")

    # Convert date for RSS (RFC 2822)
    try:
        pub_date = datetime.strptime(post_date, "%Y-%m-%d")
        pub_date_str = email.utils.format_datetime(pub_date)
        pub_date_str = pub_date_str.replace("-0000","GMT")
    except ValueError:
        pub_date_str = email.utils.format_datetime(datetime.utcnow())

    # Add post metadata for RSS
    rss_items.append({
        "title": post_name.replace("-", " ").title(),
        "link": f"{blog_url}/{html_filename}",
        "description": description,
        "pubDate": pub_date_str,
        "guid": f"{blog_url}/{html_filename}",
    })

# Finish posts page
posts_html.append("</div>")
posts_html.append("</main>")

with open(POSTS_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(posts_html))

print(f"Site built successfully in: {OUTPUT_DIR}")
build_date = email.utils.format_datetime(datetime.utcnow()).replace("-0000","GMT") 

# read rss_des_file
rss_des_txt = ""
if rss_des_file != "nill":
    try:
        with open(rss_des_file, "r", encoding="utf-8") as f:
            rss_des_txt = f.read().strip()
    except:
        print("rss_des_file dose not exist")
# --- Build RSS Feed ---
rss_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="{blog_url}">
<channel>
  <atom:link href="{blog_url}/rss.xml" rel="self" type="application/rss+xml" />
  <title>{blog_name}</title>
  <link>{blog_url}/</link>
  <description>{rss_des_txt}</description>
  <language>en-us</language>
  <lastBuildDate>{build_date}</lastBuildDate>
"""

rss_footer = """</channel>
</rss>
"""

rss_entries = []
for item in reversed(rss_items):  # newest first
    rss_entries.append(f"""  <item>
    <title>{item['title']}</title>
    <link>{item['link']}</link>
    <guid isPermaLink=\"true\">{item['guid']}</guid>
    <pubDate>{item['pubDate']}</pubDate>
    <description><![CDATA[{item['description']}]]></description>
  </item>""")

rss_xml = rss_header + "\n".join(rss_entries) + "\n" + rss_footer

with open(RSS_FILE, "w", encoding="utf-8") as f:
    f.write(rss_xml)

print(f"RSS feed written to: {RSS_FILE}")

