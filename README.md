# IndiGen
A single script static blog gernetaor that converts formatted markdown folder to posts and rolls an rss feed for you

# Examples
The maintainer made this for their own blog, https://derivativethoughts.neocities.org/.

If you have another bolg built in it let me know at derivativethoughts@proton.me

# Use

This repo is intented to be used as a template for your indiweb blog. It includes a page structure for a basic html/css blog, build.py to build the blog posts from markdown, and a github action to deploy to neocities.

## Structure

This is the intended tree structure for the blog

```
index.html      (actual base page, includes deploy/posts.html via javascript)
header.html     (header to include on each page)
footer.html     (footer to include in each page)
about.html      (site desc)
contact.html    (contact details)
not_found.html  (served if the user goes to the wrong page)
style.css       (style page for the site)
background.gif  (not included, tiled repeting gif background, see style.css)
rssdic.txt      (not included, short desc of the blog for rss)
posts           (not copied to the site via github action)
  |
  -> yyyy,mm,dd:postname
        |
        -> des.txt      (des of post)
        -> post.md      (markdown of the post)
        -> thumb.jpg    (jpg image used as a thumbnail for the post)

fonts   (empty by default)
  |
  -> myfontfile.ttf 

deploy (made by build.py)
  |
  -> posts.html     (page of post postcards to be included in other pages)
  -> rss.xml        (rss feed of posts ordered by date)
  -> postname.html  (post html page made by build.py)
  -> postname.jpg   (post thumbnail copy)
```

## Build and Test

### Dependencies
IndiGen depends on pandoc, python3, and pypandoc. Use the requierments.txt or the flake.nix to install what you need.

### Build 
`python build.py blog_url blog_name rss_des_file`

Where blog_url is the address of your blog, blog_name is the name of your blog and rss_des_file is a text file containing the description of the site to be used for the rss feed.

rss_des_file can be "nill" to have no description 

### Test

Use `python -m http.server` to test on localhost:8000

## Deploy to neocities with a github action

### Setup

You need to add your neocities api token as a github secret named "NEOCITIES_API_TOKEN". The neocities api lets programs do stuff to your site automatically.

On neocities go to settings -> manage site settings -> api -> generate api key and copy the big sting of letters and numbers in bold. Don't let other people have this unless you want them to change your site themselves.

On github Go to the repo, Settings -> Secrets and variables -> Actions -> Repository secrets and add a new one with the green button. copy the api token here. This is private place to keep data you want your public repos to use for automations.

### Use

As of now when the main branch of the github repo is updated -name html, css, txt, xml, and gif files in the root folder and the whole deploy folder will be copied to necities. Only files that are changed will be updated. See .github/workflows/deploy.yml based on the existing deploy to neocities github action found here https://github.com/marketplace/actions/deploy-to-neocities