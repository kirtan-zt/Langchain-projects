# Create two asynchronous API calls and run them together.

import asyncio
import aiohttp
import time

async def fetch_data(url, session):
    async with session.get(url) as response:
        return await response.json()

async def main():
    url1="https://jsonplaceholder.typicode.com/posts/1"
    url2="https://jsonplaceholder.typicode.com/posts/2" 

    start_time=time.time()

    async with aiohttp.ClientSession() as session:
        # Schedule both fetch operations to run concurrently
        task1 = asyncio.create_task(fetch_data(url1, session))
        task2 = asyncio.create_task(fetch_data(url2, session))

        # Wait for both tasks to complete and gather their results
        # asyncio.gather runs the awaitable objects in the tasks concurrently
        results = await asyncio.gather(task1, task2)

        data1 = results[0]
        data2 = results[1]

        print("Data from API 1 :\n", data1)
        print("-"*30)
        print("Data from API 2 :\n", data2)
    
        end_time = time.time()
        print("-"*30)
        print(f"Total time taken: {end_time - start_time:.2f} seconds")
        return results

if __name__ == "__main__":
    asyncio.run(main())
