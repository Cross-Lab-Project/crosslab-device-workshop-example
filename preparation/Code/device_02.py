import asyncio
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.api_client import APIClient

deviceUrl = 'https://api.goldi-labs.de/devices/0ace7262-ac25-44c5-a06b-8c2586ff979b'
deviceToken = 'bb022126-1b12-465e-af8d-f2c51c4f2f08'

async def main_async():
    device = DeviceHandler()
    
    async with APIClient('https://api.goldi-labs.de') as apiClient:
        apiClient.authToken = deviceToken
        await device.connect(deviceUrl, apiClient)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()