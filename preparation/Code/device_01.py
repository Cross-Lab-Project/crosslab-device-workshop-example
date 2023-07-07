import asyncio
from crosslab.soa_client.device_handler import DeviceHandler

async def main_async():
    device = DeviceHandler()
    
    await device.connect()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()