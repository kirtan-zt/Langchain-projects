# Compare execution time between sync vs async calls.

import time
import asyncio

# Synchronous functions
def brewCoffee():
    print("Start brewCoffee()")
    time.sleep(3)
    print("End brewCoffee()")
    return "Coffe is ready"

def toastBagel():
    print("Start toastBagel()")
    time.sleep(2)
    print("End toastBagel()")
    return "Bagel is toasted"

if __name__=='__main__':
    start_time=time.time()

    result_coffee=brewCoffee()
    result_bagel=toastBagel()

    end_time=time.time()
    elapsed_time=end_time-start_time
    print(f"Elapsed time in synchronous calls: {elapsed_time:.2f} seconds")

# Asynchronous functions using async and await
async def brewCoffee():
    print("Start brewCoffee()")
    await asyncio.sleep(3)
    print("End brewCoffee()")
    return "Coffe is ready"

async def toastBagel():
    print("Start toastBagel()")
    await asyncio.sleep(2)
    print("End toastBagel()")
    return "Bagel is toasted"

async def main():
    start_time=time.time()

    # create_task wraps a coroutine func in an async object and schedules it to run concurrently on the event loop
    coffee_task=asyncio.create_task(brewCoffee())
    bagel_task=asyncio.create_task(toastBagel())

    result_coffee=await coffee_task
    result_bagel=await bagel_task

    end_time=time.time()
    elapsed_time=end_time-start_time
    print(f"Elapsed time in asynchronous calls: {elapsed_time:.2f} seconds")

if __name__=='__main__':
    asyncio.run(main())