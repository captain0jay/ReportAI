import time
from DB.redis import RedisQueue
from DB.pg import DBManager
import asyncio
from crew import run_crew

async def process_task(task):
    try:
        response = await run_crew(query=task['query'], fileContent=task['fileContent'])
        db = DBManager()
        await db.add_entry(task['slug'], str(response))
        
    except Exception as e:
        print(f"Error processing task {task}: {e}")

async def main():
    q = RedisQueue('reports')
    
    while True:
        task = q.dequeue(timeout=5)
        if task:
            await process_task(task)

if __name__ == '__main__':
    print("Processor running...")
    asyncio.run(main())
