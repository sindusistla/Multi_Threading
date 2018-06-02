import itertools
import threading
import time
import multiprocessing
import os


class myThread(threading.Thread):
    def __init__(self, threadID, TransactionList, Pairs, threadLock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.Pairs = Pairs
        self.TransactionList = TransactionList
        self.threadLock = threadLock

    def run(self):
        # print("Starting ", self.threadID)
        FormPairs(self.threadID, self.TransactionList, self.Pairs, self.threadLock)
        # print("Exiting " ,self.threadID)


def Open_file(Transactions):
    dir = os.path.dirname(__file__)
    print(dir)
    filename = os.path.join(dir, "/Assignment02/TransactionData.txt");
    print("1.Open file to read the Transactions")
    fileptr = open(filename, "r")
    LineList = []
    count = 0;
    for line in fileptr:
        LineList = list(map(int, line.strip().split(' ')))
        Transactions.append(LineList)
        count = count + 1;
    'Generate threads for list of lists'
    print("Number of lines in the Data file :", count)
    print("2.Close the file")
    fileptr.close()


def FormPairs(ThreadID, TransactionList, Pairs, threadLock):
    count = 0
    tuplelist = []
    for i in range(0, len(TransactionList)):
        for k in range(i + 1, len(TransactionList)):
            for j in range(k + 1, len(TransactionList)):
                tuplelist.append((TransactionList[i], TransactionList[k], TransactionList[j]));

    # Acquire lock
    threadLock.acquire()
    Pairs.append(tuplelist)
    threadLock.release()


def main():
    Transactions = []
    Pairs = []
    TransactionThreads = []
    PairsCount = 0
    PairDictionary = {}
    start_time = time.time()

    threadLock = threading.Lock()
    print("****  Phases of Execution ****")
    # Open File
    Open_file(Transactions)
    print("3.Started Creating threads")
    for trans in range(0, len(Transactions) - 1):
        thread = myThread(trans, Transactions[trans], Pairs, threadLock)
        thread.start()
        TransactionThreads.append(thread)
    print("4.Started Joining threads")
    for t in TransactionThreads:
        t.join();
    print("5. Completed Joining threads")
    for PairList in Pairs:
        # We have pairs list her
        # print( "\n",PairList)
        for OnePair in PairList:
            PairsCount = PairsCount + 1;
            if OnePair not in PairDictionary:
                PairDictionary[OnePair] = 1;
            else:
                # That pair is present in the list
                Value = PairDictionary.get(OnePair);
                # Update with new count
                PairDictionary[OnePair] = Value + 1;
    print("6. Pairs Dictionary is Created")
    # Find max of count Count(A,B,C)
    print("----------- The Report -------------")
    maximum = max(PairDictionary, key=PairDictionary.get)
    print("The Maximum occurrence triplet is :", maximum)
    print("Frequency count :", PairDictionary[maximum])

    # Find occurence count of Count(B,C)
    # Traverse through all the transactions and Count the transactions which has both B, C in it
    BCCount = 0
    Apresent = False
    Bpresent = False
    for Tlist in Transactions:
        if maximum[1] in Tlist:
            Apresent = True
        if maximum[2] in Tlist:
            Bpresent = True
        if (Apresent == True and Bpresent == True):
            BCCount = BCCount + 1
    print("Count(A,B,C)/Count(B,C)", PairDictionary[maximum], BCCount)
    print("Probability of P(A,B,C) :", PairDictionary[maximum] / BCCount)
    print("Number of Cores of CPU:", multiprocessing.cpu_count())
    print("Execution Time :", time.time() - start_time)
    print("Exiting the Main thread Execution")


# Call the main function
main()




