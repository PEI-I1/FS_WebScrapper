from app import get
from app import getPackets
from app import getStores

def updater_phones_tariffs_packets_lapoio():
    print("[FS_SCRAPPER] Starting Update of phones, tariffs and support lines...")
    get.update()
    print("[FS_SCRAPPER] Updated phones, tariffs and support lines!")
    print("[FS_SCRAPPER] Starting Update of packages...")
    getPackets.update()
    print("[FS_SCRAPPER] Updated packages!")

def updater_lojas():
    print("[FS_SCRAPPER] Starting Update of stores...")
    getStores.update_lojas()
    print("[FS_SCRAPPER] Updated stores!")
