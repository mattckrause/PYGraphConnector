import asyncio
import os
from dotenv import load_dotenv, set_key

load_dotenv()
# suppress warnings when working locally with Dev Proxy

async def main() -> None:
    #add logic for first run vs subsequent runs
    print(os.environ.get("_firstrun"))
    if os.environ.get("_firstrun") == "true":
        print("first run")
        print("setting _firstrun to False")
        set_key('.env', '_firstrun', "false")
    else:
        print("subsequent run")

if __name__ == "__main__":
    asyncio.run(main())
