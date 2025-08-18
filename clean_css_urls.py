import re
from pathlib import Path

# Chemin absolu de ton fichier CSS
CSS_FILE = Path("/Users/marc./PycharmProjects/Python-OC-Lettings-FR/static/css/styles.css")

# Regex pour matcher url(...)
url_re = re.compile(r"url\((['\"]?)([^)'\"]+)\1\)")

def is_external(url: str) -> bool:
    url = url.strip()
    return url.startswith(("http://", "https://", "data:"))

def main():
    if not CSS_FILE.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {CSS_FILE}")

    css_text = CSS_FILE.read_text(encoding="utf-8")
    new_css = css_text

    for _, url in url_re.findall(css_text):
        url = url.strip()
        if is_external(url) or url.startswith("/"):
            continue

        candidate = (CSS_FILE.parent / url).resolve()
        if not candidate.exists():
            print(f"❌ Supprime référence manquante: {url}")
            for pattern in [f"url({url})", f"url('{url}')", f'url("{url}")']:
                new_css = new_css.replace(pattern, "none")

    CSS_FILE.write_text(new_css, encoding="utf-8")
    print(f"✅ Nettoyage terminé : {CSS_FILE} mis à jour.")

if __name__ == "__main__":
    main()