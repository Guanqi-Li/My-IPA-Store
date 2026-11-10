# My IPA Store

Free personal-use IPA catalog. Stores IPA files in GitHub Releases and publishes a static directory and JSON source through GitHub Pages.

**Format:** AltStore Classic-style JSON, not a special format for any particular signing app. There is no JSON source format supported by all iOS signing apps. Clients must explicitly support this format.

## Setup

1. Change repository visibility to Public (Settings > General > Danger Zone > Change repository visibility). Public source data and IPA downloads are visible to anyone.
2. Set Settings > Pages > Source to **GitHub Actions**.
3. Run Actions > **Publish software source** > **Run workflow**.
4. Web catalog: https://guanqi-li.github.io/My-IPA-Store/
5. JSON source: https://guanqi-li.github.io/My-IPA-Store/source.json

## Add IPA from a URL

Run **Actions > Import IPA from URL** and enter a direct HTTPS IPA URL (not a web share page). The Action downloads, inspects, uploads to Releases and updates the JSON source automatically.

## Add a local IPA

Install Python 3 and GitHub CLI, authenticate with `gh auth login`, clone this repository, then:

```sh
python scripts/manage.py add --file "/path/to/App.ipa" --repo Guanqi-Li/My-IPA-Store --description "About this app"
git add docs/source.json
git commit -m "Add app"
git push
```

The tool reads app name, identifier, version and build from Info.plist and records file size. Icons often reside in Assets.car and **are not extracted automatically**; supply `--icon` for an icon URL. Multiple builds/versions share one app entry.

## Limits

- Single Release asset must be smaller than 2 GiB. Overall Releases may exceed 50 GB but do not have an unconditional capacity or service guarantee.
- GitHub access and download performance in mainland China are inconsistent and **not guaranteed without a proxy**.
- Pages hosting and public Release assets are public, even when you intend to be the only user.
- Never upload private signing certificates, credentials or personal content.
- Use GitHub Releases to delete outdated assets; deleting a source entry does not remove its stored IPA.
