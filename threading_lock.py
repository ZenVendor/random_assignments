import random
import time
import threading
import math

no_of_books = 200
no_of_readers = 20
books_per_reader = 40
selected_books = math.ceil(books_per_reader * 1.6)

class Book:
    def __init__(self, id):
        self.id = id
        self.pages = random.randint(50, 500)
        self.lock = threading.Lock()
        self.checked_out_by = None

    def checkout(self, reader_id):
        if self.lock.locked():
            print("Book {} is checked out by reader {}.".format(self.id, self.checked_out_by))
            return 0
        else:
            self.lock.acquire()
            self.checked_out_by = reader_id
            print("Reader {} is checking out book {}.".format(reader_id, self.id))
            return 1
    
    def checkin(self):
        print("Book {} returned by reader {}.".format(self.id, self.checked_out_by))
        self.lock.release()
        self.checked_out_by = None
        

class Reader:
    def __init__(self, id):
        self.id = id
        self.to_read = []
        self.read = []
    
    def select_books(self, bookshelf):
        bookset = set(random.choices(bookshelf, k=selected_books))
        self.to_read = list(bookset)[0:books_per_reader]
    
    def read_books(self):
        while (self.to_read):
            for book in self.to_read:
                print("Reader {} wants to read book {}".format(self.id, book.id))
                if book.checkout(self.id):
                    print("Reader {} started reading book {}".format(self.id, book.id))
                    time.sleep(book.pages/1000)
                    print("Reader {} finished reading book {}".format(self.id, book.id))
                    book.checkin()
                    self.read.append(book)
            for book in self.read:   
                if book in self.to_read:
                    self.to_read.remove(book)
        print("Reader {} has no more books to read".format(self.id))
            

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
    print("Running thread for reader {}.".format(reader.id))
    task.start()



