import asyncio
import logging
import contextlib

from config import SLEEP_SECONDS, EXCHANGES
from data_miner import DataMiner
from shared_modules.acc import ACC


async def main() -> None:
    # Logging
    logging.basicConfig(
        filename='researcher.log',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Analyzer
    dm = await ACC.create(DataMiner, EXCHANGES)
 
    # Main loop
    async with dm:
        logging.info("DM STARTED")

        while True:
            await dm.receive_messages()
            await dm.serve_subscriptions()
            await asyncio.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
