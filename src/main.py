import sys
import asyncio

sys.path.append('./src/services/data_miner/app')
import services.data_miner.app.main as data_miner


if __name__ == "__main__":
    asyncio.run(data_miner.main())
