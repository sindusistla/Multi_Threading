# Student Name : Jaya Sistla
#Assignment 02
#Multithreading
#----------------------------------------------------------------------------------------

# Import necessary libraries
import threading
import time
import operator
import time
import multiprocessing
import os

# Multithreading Class, the thread we create in our implementation is object of thie class
class myThread (threading.Thread):
    # Intialize the thread with neccesary Attributes with which we are going to start the thread
  def __init__(self, threadID, TransactionList,Pairs,threadLock):
     threading.Thread.__init__(self)
     self.threadID = threadID
     self.Pairs=Pairs
     self.TransactionList=TransactionList
     self.threadLock=threadLock

    # If thread is executed what should it run,
     # in our case it thread should execute to form pairs of transactions
  def run(self):
     #print("Starting ", self.threadID)
     FormPairs(self.threadID, self.TransactionList, self.Pairs,self.threadLock)
     #print("Exiting " ,self.threadID)

# Implementation of the function which forms pairs of transactions
def FormPairs(threadID, TransactionList, Pairs,threadLock):
   tuplelist=[]
   for i in range(0,len(TransactionList)):
       for k in range(i+1,len(TransactionList)):
           tuplelist.append((TransactionList[i],TransactionList[k]));
   threadLock.acquire()
   Pairs.append(tuplelist);
   threadLock.release();

# Routine to Open the file to read transactions
def Open_file(Transactions):
  dir = os.path.dirname(__file__)
  filename = os.path.join(dir,"TransactionData.txt");
  LineList = []
  count=0;

# Open the file transactionData.txt to read the files
  print("1.Opening File")
  fileptr = open(filename, "r")
  for line in fileptr:
      LineList = list(map(int, line.strip().split(' ')))
      Transactions.append(LineList)
      count=count+1;
  print("2.Number of lines in the Transaction Data file : ",count)
  fileptr.close();
  print("3.Closing File")

# Find the Count of Transaction A to find COnditional Probability
def findCountofA(NumA,Transactions):
   CountA=0
   for tranlist in Transactions:
       for t in tranlist:
           if (t==NumA):
               CountA=CountA+1
   return CountA

def main():
    Transactions = []
    TransactionThreads=[]
    Pairs=[]
    PairsList=[]
    PairDictionary ={}
    ProbabilityPairs={}
    threadCount=0
    Start_time =time.time()
    print("**** Phases of Execution ****")
    # Frist open the file and read the contents into a list of lists
    Open_file(Transactions)

    # Create a Thread Lock
    threadLock = threading.Lock()

    print("4.Started Created Threads")
    for trans in range(0,len(Transactions)-1):
       'Create and start threads'
       thread =myThread(trans, Transactions[trans], Pairs,threadLock)
       thread.start()
       threadCount=threadCount+1
       TransactionThreads.append(thread)

    # Join the threads
    print("4.Started Closing Threads")
    for t in TransactionThreads:
       t.join();

    print("5.Completed Joining threads")
    PairsCount=0
    # Now we have all the pairs in Pairs list add them to a dictionary traverse through the pairs dictionary
    # Find the Number of occurences
    for PairList in Pairs:

       # We have pairs list her
       for OnePair in PairList:
           PairsCount=PairsCount+1;
           if OnePair not in PairDictionary:
               PairDictionary[OnePair]=1;
           else:
               # That pair is present in the list
               Value=PairDictionary.get(OnePair);
               # Update with new count
               PairDictionary[OnePair]=Value+1;
    print("6.Pairs Dictionary is formed")
    print("-------------- The Report-------------------------")
    # Find the maximum occurence count of pair
    maximum = max(PairDictionary, key=PairDictionary.get)
    print("The maximum is :",maximum, PairDictionary[maximum])
    # Find the number of occurrences of

    CountofA=findCountofA(maximum[0],Transactions)

    print("Probability of P(%d/%d) -> " %(maximum[1],maximum[0]))
    print ("[%d/%d] -> " %(PairDictionary[maximum],CountofA))
    print(" Probability is -> ",float(float(PairDictionary[maximum])/float(CountofA)))
    print("Number of CPU Cores Count:",multiprocessing.cpu_count())
    print("Number of threads created :",threadCount)
    print("Execution time: ",time.time()-Start_time)
    print("-----------------------------------------------")
    print("Exiting Main Thread")

# Call Main function
main()