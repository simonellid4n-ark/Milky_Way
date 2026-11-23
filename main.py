import asyncio
from game import MilkyWayGame


async def main():
    game = MilkyWayGame()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())