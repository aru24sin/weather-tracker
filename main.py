import python_weather
import asyncio
import os

async def getweather() -> None:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('Michigan')
        print(weather.temperature)

        for daily in weather:
            print(daily)

            for hourly in daily:
                print(f' --> {hourly!r}')
            break

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(getweather())