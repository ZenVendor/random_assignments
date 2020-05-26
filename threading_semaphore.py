import random
import time
import threading

no_of_books = 200
no_of_readers = 20
books_per_reader = 40
book_copies = 4

class Book:
    def __init__(self, id):
        self.id = id
        self.pages = random.randint(50, 500)
        self.checkout = threading.BoundedSemaphore(book_copies)
        self.checked_out_by = []
   
class Reader:
    def __init__(self, id):
        self.id = id
        self.to_read = []
    
    def select_books(self, bookshelf):
        while len(self.to_read) < books_per_reader:
            book = random.choice(bookshelf)
            if book not in self.to_read:
                self.to_read.append(book)
    
    def read_books(self):
        for book in self.to_read:
            print("Reader {} wants to read book {}".format(self.id, book.id))
            book.checkout.acquire()
            print("Reader {} started reading book {}".format(self.id, book.id))
            time.sleep(book.pages/100)
            print("Reader {} finished reading book {}".format(self.id, book.id))
            book.checkout.release()

bookshelf = []
for i in range(no_of_books):
    bookshelf.append(Book(i))

readers = []
for i in range(no_of_readers):
    readers.append(Reader(i))
    readers[i].select_books(bookshelf)

for reader in readers:
    print("Creating thread for reader {}.".format(reader.id))
    task = threading.Thread(target=reader.read_books)
    task.start()
