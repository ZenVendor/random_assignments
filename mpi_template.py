from mpi4py import MPI

# Te zmienne są potrzebne.
comm = MPI.COMM_WORLD       # tu są metody MPI
rank = comm.Get_rank()      # to pobiera numer procesu: 0 - master, reszta slave
size = comm.Get_size()      # to jest ilość dostępnych procesów
status = MPI.Status()       # to wysyłane jest przez proces, zawiera m.in. numer procesu i tag

# ustawiamy ilość slavów - pracowników, żeby master wiedział kiedy skończyć - czyli dostępne procesy - 1(bez mastera)
workers = size-1

if rank == 0:       # tę część będzie robić master
    data = None     # inicjalizacja zmiennej data potrzebna w tym miejscu

    # master wykonuje w kółko te same czynności dopóki nie każe wszystkim pracownikom zakończyć się
    while workers > 0:

        # ustawia się w tryb odbioru i czeka na zgłoszenie się pracownika
        comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)

        # jak otrzyma zgłoszenie pobiera ze statusu numer pracownika
        worker = status.Get_source()

        # jeśli jest jeszcze praca do wykonania to przesyła ją do pracownika
        # w jaki sposób to jest sprawdzane zależy od rodzaju pracy i implementacji
        if work_to_be_done:

            # wybiera część danych dla pracownika
            data = piece_of_data
            # i wysyła je z tagiem majacym oznaczać "wykonaj to"
            # tagi można ustalić jak się chce, a przy większej komplikacji przypisać do stałych globalnych
            # czyli wyślij dane, do pracownika z numerem pobranym z jego statusu, z tagiem "pracuj"
            comm.send(data, dest=worker, tag=1)

        # jak nie ma pracy, każe pracownikowi zakończyć działanie
        else:

            # jak wyżej, ze statusem "zakończ"
            comm.send(data, dest=worker, tag=9)
            # zmniejsza liczbę dostępnych pracowników
            workers -= 1


# ta część jest dla pracowników
else:
    data = None         # inicjalizacja zmiennej data

    # pracownik będzie powtarzał te same czynności dopóki master mu nie każe zakończyć
    while True:

        # zgłasza się do mastera - data jest wymagane, cel jest 0 - master, tag nie ma znaczenia w tym wypadku
        comm.send(data, dest=0, tag=0)

        # i czeka na odpowiedź z danymi, od mastera, z jakimkolwiek tagiem
        incoming = comm.recv(data, source=0, tag=MPI.ANY_TAG, status=status)

        # ze statusu pobiera tag
        # jeśli tag mówi "wykonaj", wykonuje swoje zadanie
        if status.Get_tag() == 1:

            # instrukcje do wykonania

        # jeśli tag mówi "zakończ"
        else:
            break       # wychodzi z pętli

#---------
# KONIEC
#---------

# W przykładowym kodzie wyniki były jeszcze zwracane masterowi, który je wpisywał do pliku - ja tego już nie robiłem


# Zakończenie pracownika można zrobic również za pomocą flagi:
# czyli zamiast break dodajemy zmienną flagi pod else:
else:
    action_flag = 1

    # zamiast while True sprawdzamy flagę
    while action_flag == 1:

    # instrukcje
    # i w przypadku tagu nakazujacego zakończenie
        else:
            action_flag = 0

# -----------

# w "oryginale" tagi liczbowe były przypisane dla łatwiejszego użycia do stałych globalnych
# np.

TAG_WORK = 1
TAG_END = 9

# i w każdym miejscu gdzie jest używany tag wpisujemy nazwę zmiennej a nie liczbę, co jest bardziej czytelne.

# -----------

# W moim przykładzie dane są rozdzielane następująco

# na początku wczytujemy linie z adresami z pliku
domains = open("domains.txt", "r").readlines()

# są one umieszczane w liście:
['adres1', 'adres2']

# do sprawdzenia czy jest jeszcze praca sprawdzam, czy lista zawiera jeszcze jakieś elementy
if domains:     # to jest równoznaczne "if domains is not None"

# natomiast w czasie przydzielania pracy wyciągam element z listy
# pop() czyta element, po czym usuwa go z listy
# rstrip() usuwa spacje i niewidoczne znaki z początku i końca - bardziej dla porządku niż jakiegoś wymogu programu
data = domains.pop().rstrip()
# data w tym momencie zawiera jeden adres strony i to jest wysyłane do pracownika


# po stronie pracownika wykonuje poniższe:
# wysyłam http request do przydzielonego adresu i zwracam tekst strony (html)
page = requests.get(incoming).text

# tworzę obiekt BS, który może byc przetwarzany przy pomocy metod tego modułu
soup = BeautifulSoup(page, features="html.parser")

# znajduję wszystkie elementy H1 i H2 - wynikiem jes lista
headers = soup.find_all(["h1", "h2"])

# każdy element listy wypisuję na ekran, znów usuwając niewidzialne znaki i spacje
for item in headers:
    print("lists header: %s" % (item.text.rstrip()))

