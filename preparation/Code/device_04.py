import asyncio
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.api_client import APIClient

from crosslab.soa_services.file import FileService__Consumer, FileServiceEvent
from crosslab.soa_services.electrical import ElectricalConnectionService
from crosslab.soa_services.electrical.signal_interfaces.gpio import ConstractableGPIOInterface, GPIOInterface

deviceUrl = 'https://api.goldi-labs.de/devices/cbd87f5f-da6b-47f4-9529-b41575752d22'
deviceToken = 'aa44a2c2-7d9d-4fcc-9587-e042ff826d9c'

code = ""
setRed = lambda x: None
setGreen = lambda x: None
setYellow = lambda x: None

async def interpreter():
    while True:
        try:
            eval(code)
        except:
            pass
        await asyncio.sleep(0.1)

async def main_async():
    device = DeviceHandler()

    fileService = FileService__Consumer('program')
    @fileService.on('file')
    def onFile(event: FileServiceEvent):
        global code
        code = event['content']

    device.add_service(fileService)

    electricalService = ElectricalConnectionService('Ampel')
    electricalService.addInterface(ConstractableGPIOInterface(['red', 'green', 'yellow']))
    # electricalService.on("newInterface", newAmpelInterface)
    device.add_service(electricalService)
    
    async with APIClient('https://api.goldi-labs.de') as apiClient:
        apiClient.authToken = deviceToken
        interpreterTask = asyncio.create_task(interpreter())
        deviceHandlerTask = asyncio.create_task(device.connect(deviceUrl, apiClient))
        await deviceHandlerTask

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()