# derrickzhao.com

Personal portfolio for Derrick Zhao. Plain HTML and CSS, no build step, hosted on GitHub Pages.

```
index.html                 Home: intro, selected work, experience, tools, about, contact
projects/*.html            One case study per project
projects/_template.html    Copy this to add a new project
assets/css/site.css        All styling (colors and fonts are at the top)
assets/js/site.js          Shows a placeholder frame for any image not added yet
assets/img/                Project images (filled by tools/fetch_images.py)
assets/Derrick_Zhao_Resume.pdf   Add your resume here (linked from the nav)
404.html                   Shown for old Google Sites links
.nojekyll                  Tells GitHub Pages to serve files as-is
```

## 1. Put it on GitHub

1. Create a new public repository named **`<your-github-username>.github.io`**.
2. Upload everything in this folder (on github.com: **Add file → Upload files**, drag the folder contents in, commit). Or with git:
   ```
   git init
   git add .
   git commit -m "Portfolio site"
   git branch -M main
   git remote add origin https://github.com/<username>/<username>.github.io.git
   git push -u origin main
   ```
3. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`.
4. After a minute or two the site is live at `https://<username>.github.io`.

## 2. Bring over the images (do this before turning off Google Sites)

```
python tools/fetch_images.py
```

This downloads the images from the current Google Sites pages into `assets/img/` with the file names the pages expect. Commit and push them. Any frame still showing diagonal hatching on the site is an image that's missing; the frame tells you the exact path to put it at.

## 3. Add your resume

Save your resume as `assets/Derrick_Zhao_Resume.pdf`. Remove your phone number from the public copy if you don't want it scraped.

## 4. Move derrickzhao.com from Google Sites to GitHub

Only do this once the GitHub version looks right.

1. In Google Sites, remove the custom domain from the site (Settings → Custom domains).
2. At your domain registrar's DNS settings, delete the old Google records for `www` and the root domain, then add:
   - `CNAME` record: host `www` → `<username>.github.io`
   - `A` records: host `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. In the repo: **Settings → Pages → Custom domain**, enter `www.derrickzhao.com`, save. GitHub adds a `CNAME` file for you.
4. When the DNS check passes, tick **Enforce HTTPS**.
5. Recommended: verify the domain under your GitHub account **Settings → Pages** so nobody else can claim it.

DNS changes can take a few hours. GitHub's current IP addresses are listed in their Pages docs under "Managing a custom domain" if anything changes.

## Editing

- **Text:** edit the HTML directly. Every page shares the same header and footer markup, so if you change the nav, change it in each file.
- **New project:** copy `projects/_template.html` to `projects/<name>.html`, fill it in, put images in `assets/img/<name>/`, then copy one `<article class="work-item">` block in `index.html` and point it at the new page. Update the previous/next links at the bottom of the neighbouring project pages.
- **Colors and fonts:** the variables at the top of `assets/css/site.css`. Dark mode colors are right below.
- **TODO comments:** search the files for `TODO` to find spots that need your input.
- **Preview locally:** open `index.html` in a browser, or run `python -m http.server` in this folder and visit `http://localhost:8000`.
