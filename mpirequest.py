from mpi4py import MPI
from bs4 import BeautifulSoup
import requests

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()

domains = open("domains.txt", "r").readlines()
workers = size-1


if rank == 0:
    data = None

    while workers > 0:
        comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        worker = status.Get_source()
        print("[Dispatch] contacted by worker %d" % worker)
        if domains:
            print("[Dispatch] gives work to worker %d." % worker)
            data = domains.pop().rstrip()
            comm.send(data, dest=worker, tag=1)
        else:
            print("[Dispatch] retires worker %d." % worker)
            comm.send(data, dest=worker, tag=9)
            workers -= 1

else:
    data = None
    while True:
        comm.send(data, dest=0, tag=0)
        incoming = comm.recv(data, source=0, tag=MPI.ANY_TAG, status=status)

        if status.Get_tag() == 1:
            print("[Worker %d] received %s" % (rank, incoming))
            soup = BeautifulSoup(requests.get(incoming.rstrip()).text, features="html.parser")
            for item in soup.find_all(["h1", "h2"]):
                print("[Worker %d] lists header: %s" % (rank, item.text.rstrip()))
        else:
            print("[Worker %d] retired." % rank)
            break
