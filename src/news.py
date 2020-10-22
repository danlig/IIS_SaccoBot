from feedparser import parse as fdparse
from bs4 import BeautifulSoup
from telegram import ParseMode
import os

last_news = ""

def check_updates(bot):
    """Controlla nuovi updates."""
    # LOG: CHECKING
    print("[CHECKING] Controllando nuove news...")

    # Ottieni info ultima news
    info = get_news(0)

    # Inizializza news locale
    global last_news

    if last_news == "":
        # Se prima chiamata:
        #   Salva localmente url ultima news
        last_news = info['page']

        # LOG: CHECKED
        print("[CHECKED] Ultima news salvata localmente") 
    elif last_news != info['page']:
        # Se locale e online non coincidono:
        #   Nuova news rilevata
        # LOG: CHECKED
        print("[CHECKED] Rilevata nuova news")

        # Inizializza caption documento
        caption = "<b>" + info['title'] + "  </b>\n" + \
            "\n🗓  Data: " + info['published'] + "\n" + \
            "\n📄  Pagina: " + info['page']

        # Aggiungi allegati
        for attcs in info['attcs']:
            caption += "\n\n📎  Allegato: " + attcs

        # Aggiungi tags
        caption += "\n\n"
        for tag in info['tags']:
            caption += f"#{tag}  "

        # Condividi news sul canale
        bot.send_message(chat_id=os.environ['CHANNEL_ID'], text=caption, 
                                    parse_mode=ParseMode.HTML)

        # Aggiorna news locale
        last_news = info['page']

        # LOG: SHARE
        print("[SHARE] Pubblicata nuova news")
    else:
        # Nessuna news
        # LOG: CHECKED
        print("[CHECKED] Nessuna nuova news trovata")     

def get_news(i):
    """Ottieni news di posizione i."""
    # Inizializza feed url
    FEED_URL = "https://www.iis-sacco.edu.it/feed/"

    # Parse del feed xml
    feed = fdparse(FEED_URL)
    # Ottieni singola news
    item = feed.entries[i]

    # Ottieni titolo
    title = item.title
    # Ottieni data di upload
    published = item.published[5:-15]
    # Ottieni url della pagina news
    page = item.link
    # Ottieni tags
    tags = [t.term.replace(" ", "").replace("-", "") 
                for t in item.get('tags', [])]

    # Ottieni pagina html
    html = item.content[0].value
    soup = BeautifulSoup(html, 'html.parser')
    # Scraping url dei file allegati
    attcs = [a.get('href') 
                for a in soup.find_all(class_="mtli_attachment")]

    # Restituisci info
    info = {'title': title, 'page': page, 'published': published,
                'attcs': attcs, 'tags':tags}
    return info