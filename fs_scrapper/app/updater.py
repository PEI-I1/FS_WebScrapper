from app import get
from app import getPackets
from app import getStores

def updater_phones_tariffs_packets_lapoio():
    get.update()
    getPackets.update()

def updater_lojas():
    getStores.update_lojas()
