import asyncio
import os
from dotenv import load_dotenv, set_key

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def main() -> None:
    logging.info('This is an info message')
    logging.debug('This is a debug message')
    logging.error('This is an error message')

if __name__ == "__main__":
    asyncio.run(main())
