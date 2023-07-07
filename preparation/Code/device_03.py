import asyncio
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.api_client import APIClient

from crosslab.soa_services.file import FileService__Consumer, FileServiceEvent

deviceUrl = 'https://api.goldi-labs.de/devices/cbd87f5f-da6b-47f4-9529-b41575752d22'
deviceToken = 'aa44a2c2-7d9d-4fcc-9587-e042ff826d9c'

async def main_async():
    device = DeviceHandler()

    fileService = FileService__Consumer('program')
    @fileService.on('file')
    def onFile(event: FileServiceEvent):
        print(event['content'])

    device.add_service(fileService)
    
    async with APIClient('https://api.goldi-labs.de') as apiClient:
        apiClient.authToken = deviceToken
        print(device.get_service_meta())
        await device.connect(deviceUrl, apiClient)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()