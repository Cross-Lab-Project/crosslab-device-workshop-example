import asyncio
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.api_client import APIClient

from crosslab.soa_services.file import FileService__Consumer, FileServiceEvent
from crosslab.soa_services.electrical import ElectricalConnectionService
from crosslab.soa_services.electrical.signal_interfaces.gpio import ConstractableGPIOInterface, GPIOInterface
from crosslab.soa_services.webcam import WebcamService__Producer, GstTrack

deviceUrl = 'https://api.goldi-labs.de/devices/cbd87f5f-da6b-47f4-9529-b41575752d22'
deviceToken = 'aa44a2c2-7d9d-4fcc-9587-e042ff826d9c'

code = ""
setRed = lambda value: None
setGreen = lambda value: None
setYellow = lambda value: None

async def interpreter():
    global setRed, setGreen, setYellow
    d = dict()
    while True:
        try:
            exec(code, globals(), d)
        except Exception as e:
            print(e)
        await asyncio.sleep(1)

def newAmpelInterface(interface):
    global setRed, setGreen, setYellow
    if isinstance(interface, GPIOInterface):
        interface.changeDriver('strongL')
        def set(value):
            if value:
                interface.changeDriver("strongH")
            else:
                interface.changeDriver("strongL")
        if interface.configuration['signals']['gpio'] == 'RedLight':
            setRed = set
        if interface.configuration['signals']['gpio'] == 'GreenLight':
            setGreen = set
        if interface.configuration['signals']['gpio'] == 'YellowLight':
            setYellow = set
                

async def main_async():
    device = DeviceHandler()

    fileService = FileService__Consumer('program')
    @fileService.on('file')
    def onFile(event: FileServiceEvent):
        global code
        code = event['content']

    device.add_service(fileService)

    electricalService = ElectricalConnectionService('Ampel')
    electricalService.addInterface(ConstractableGPIOInterface(['RedLight', 'GreenLight', 'YellowLight']))
    electricalService.on("newInterface", newAmpelInterface)
    device.add_service(electricalService)

    webcamService = WebcamService__Producer(
        GstTrack("videotestsrc is-live=true pattern=ball ! videoconvert ! queue ! openh264enc "), 'webam')
    device.add_service(webcamService)
    
    async with APIClient('https://api.goldi-labs.de') as apiClient:
        apiClient.authToken = deviceToken
        interpreterTask = asyncio.create_task(interpreter())
        deviceHandlerTask = asyncio.create_task(device.connect(deviceUrl, apiClient))
        await deviceHandlerTask

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()