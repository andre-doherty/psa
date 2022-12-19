import multiprocessing as mp,os

def process(line):
    print('.')

def process_wrapper(chunkStart, chunkSize):
    with open("rockyou.txt", encoding="iso8859-1", errors='ignore') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            process(line)

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

def launch():
    #init objects
    cores = 4
    pool = mp.Pool(cores)
    jobs = []

    #create jobs
    for chunkStart,chunkSize in chunkify("rockyou.txt"):
        jobs.append( pool.apply_async(process_wrapper,(chunkStart,chunkSize)) )

    #wait for all jobs to finish
    for job in jobs:
        job.get()

    #clean up
    pool.close()


if __name__ == '__main__':
    launch()