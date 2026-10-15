# novisutd.org: Novis A Cappella's website

This repository **is** the website. GitHub Pages publishes whatever is on the
`master` branch to **https://novisutd.org**, usually within a minute or two of a
change. You don't need to install anything. Every task below can be done in the
GitHub website: open a file, click the pencil icon to edit, then **Commit changes**.

> This file is not shown on the website. It's the handoff guide for whoever
> runs the website next. Please keep it up to date.

---

## Every new semester (about 15 minutes)

1. **Save the original photos in the Officer Drive.** Put the full-size headshots
   and group photo in a folder like `Website Archive/f27/`. The website only
   keeps small copies.
2. **Upload the new headshots.** On your computer, put the new photos in one
   folder named for the semester, for example `f27`. Name each photo
   `<semester>-<firstname>.jpg`, e.g. `f27-jaden.jpg` (lowercase, no spaces).
   Then in GitHub, open `img/headshots/`, click **Add file → Upload files**, and
   drag the **whole `f27` folder** onto the page. GitHub keeps the folder name,
   so the photos land in `img/headshots/f27/`.
   - Don't resize them first. An automatic GitHub Action shrinks them after you
     upload (see [Automations](#automations)).
   - If your browser won't let you drop a folder: click **Add file → Create new
     file**, type `f27/.keep` as the file name (typing `/` makes a folder),
     commit it, then open the new `f27` folder and upload the photos there.
3. **Make the new roster file.** Open the previous semester's roster (for
   example `_data/roster/f26.yml`) and click the **Copy raw file** button at
   the top right of the file. Go back to `_data/roster/`, click **Add file →
   Create new file**, name it for the new semester (`f27.yml`), paste, then
   change the names, photos and roles. The comments at the top of the file
   explain the format.
4. **Switch the site to the new semester.** In `_config.yml`, change
   `semester: f26` to `semester: f27`.
5. **New group photo?** Upload it to `img/splash/` as `f27-splash.jpg` and set
   `splash: f27-splash.jpg` in `_config.yml`.
6. **Flip the switches you need** (auditions open or closed, banner, Valentunes).
   See the next section.
7. **Check it worked.** Open the **Actions** tab. The newest
   "pages build and deployment" run should have a green check. Then open
   novisutd.org (refresh twice; it can take a minute).

Old semesters' roster files can stay in `_data/roster/`. They're a free record
of who was in Novis each semester.

---

## The settings file: `_config.yml`

Everything that changes during the year is a setting near the top of
`_config.yml`. `true` means show or on, and `false` means hide or off.

| Setting | What it does |
|---|---|
| `semester` | Which roster and photo folder to show, e.g. `f26` (Fall 2026) or `s27` (Spring 2027). Also used in the audition text ("closed for Fall 2026"). |
| `splash` | The big group photo at the top (a file inside `img/splash/`). |
| `show_about`, `show_auditions`, `show_members`, `show_content` | Show or hide each section of the home page. Its menu link hides too. |
| `auditions_open` | `false` shows "auditions are closed" with the interest form. `true` shows "auditions are open" with the sign-up link. |
| `interest_form` | Link to the interest Google Form (shown when auditions are closed). |
| `audition_signup` | Link to the audition time-slot sign-up (shown when auditions are open). |
| `show_banner`, `banner_text` | The yellow announcement bar under the top photo. |
| `show_valentunes`, `valentunes_form` | The pink Valentunes box. Turn it on in February. |
| `program_link` | Where "the program for our latest concert" links. Leave it as `/concert`. |
| `contact_email` | Email shown in the Content section. |

`semester` must be exactly one lowercase letter (`f` or `s`) followed by two
digits, like `f26` or `s27`. Anything else (for example `F26` or `fall26`)
stops the build with an error that names this rule, and the live site stays on
its last good version.

Rules for editing YAML files (`.yml`):
- Keep the spaces at the start of each line exactly as they are.
- Put text that contains `:` or `#` in "quotes".
- If you get stuck, compare your edit with the line above it.

---

## Concert programs

- Programs live in `concerts/` and are named by semester: `s22.html`,
  `f22.html`, `s23.html`, `f23.html`, `s24.html`. Their artwork is in
  `img/concerts/<semester>/`.
- **novisutd.org/concert** always opens the current program, so it's safe to
  print on posters and QR codes. To change which program it opens, edit the
  one `redirect_to:` line in `concert.html`.
- To add a program, copy the newest one (e.g. `concerts/s24.html`) to
  `concerts/<semester>.html`, edit the songs, then update `concert.html`.
- Old addresses (like `/f23 concert.html`) still work because of the
  `redirect_from:` lines at the top of each program. Please don't remove them.

---

## Photos and file names

- **Name format:** season letter + 2-digit year: `f` = fall, `s` = spring.
  `f26` = Fall 2026. Use lowercase letters, no spaces, and `.jpg`.
- **Why lowercase matters:** GitHub Pages treats `photo.JPG` and `photo.jpg` as
  different files. Your laptop doesn't, so a mismatch works for you but breaks
  on the real site. The link-check Action catches this.
- **Sizes:** headshots fit within 600×800 pixels (about 60–120 KB each), and
  the top photo is 1920 pixels wide (about 400 KB). The automation does this
  for headshots. For other images, use the free https://squoosh.app.
- **Full-size originals** belong in the Officer Drive, not in this repository.
  Every older file still exists in this repository's history even after it's
  deleted.

---

## Automations

These run by themselves in the **Actions** tab:

- **Optimize headshots** runs when photos are added under `img/headshots/` on
  `master`. It rotates them correctly, shrinks them to fit 600×800, converts
  the colors to standard sRGB, removes hidden data (like location), makes file
  names lowercase `.jpg`, and saves the result back. It can also be started by
  hand: Actions → Optimize headshots → Run workflow.
- **Check links and images** builds the site the way GitHub Pages does and
  fails (red X) if any page points at a file that doesn't exist, including
  wrong capitalization.

---

## If something goes wrong

- **Red X on "pages build and deployment"** means the change was **not**
  published. The live site keeps its last good version, so nothing is broken
  for visitors. Click the red run to read the error. Common messages:
  - `ERROR-no-roster-file-for-this-semester`: `semester:` in `_config.yml`
    doesn't match a file in `_data/roster/`.
  - `ERROR-officer-role-does-not-match-officer_roles`: a member's `role:` is
    spelled differently from the `officer_roles:` list in the roster file.
  - `ERROR-a-member-is-missing-a-photo`: someone in the roster file has no
    `photo:` line.
  - `ERROR-semester-setting-must-look-like-f26-or-s27`: fix `semester:` in
    `_config.yml`.
  - `YAML Exception` or `front matter`: there is a typo between the `---`
    lines at the top of a page, often a missing closing quote.
- **Red X on "Check links and images"** means the change **was** published,
  but a page now points at a file that doesn't exist (for example a photo name
  typo, or a concert redirect to a page that isn't there). Visitors can see the
  problem, so fix it right away. Click the red run to see which link is broken.
- **A photo doesn't show:** check its name in the roster file matches the file
  exactly, including lowercase and `.jpg`.
- **Undo a change:** open the commit on GitHub and use **Revert**, or edit
  the file back.

---

## Accounts and ownership (important for handoff)

- **Domain:** `novisutd.org` is registered through **Squarespace Domains**.
  It was originally bought through Google Domains, which Squarespace took over.
  It was registered Jan 16, 2022 and **expires Jan 16, 2027**. Make sure
  auto-renew is on and that more than one officer can log in to that account.
  Write down who owns it in the officer handoff doc (not here; this repository
  is public).
- **GitHub:** keep at least **two current officers** as owners of the
  NovisACappella GitHub organization, so access is never lost when someone
  graduates.
- `audition.novisutd.org` points at Squarespace and currently shows an
  error page. Either delete that DNS record in Squarespace, or forward it to
  the audition form.

---

## Folder map

```
_config.yml          settings and on/off switches (edit this)
_data/roster/        one roster file per semester (edit this)
index.html           home page template (rarely needs editing)
styles.css           home page styles
concert.html         /concert → current program (one line to edit)
concerts/            concert programs, their stylesheet and scripts
img/headshots/<sem>/ member photos for each semester
img/splash/          big group photos for the top of the home page
img/concerts/<sem>/  concert program artwork
img/presskit/        logo
img/social/          social media icons
.github/workflows/   the automations described above
```

## Previewing a change before it goes live (optional)

Make the change on a new branch (GitHub offers this when you commit), then
open a pull request. The link check runs on it, and you can merge when it's
green. Advanced: install Ruby, then create a file named `Gemfile` (it's kept off
the website) containing:

```
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "webrick"
```

and run `bundle install`, then `bundle exec jekyll serve`, and open
http://localhost:4000.
