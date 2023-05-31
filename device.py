import asyncio
from crosslab.soa_client.device_handler import DeviceHandler # pip install crosslab-soa-client
from crosslab.api_client import APIClient # pip install crosslab-api-client

from crosslab.soa_services.file import FileService__Consumer, FileServiceEvent # pip install crosslab-soa-service-file
from crosslab.soa_services.electrical import ElectricalConnectionService # pip install crosslab-soa-service-electrical
from crosslab.soa_services.electrical.signal_interfaces.gpio import ConstractableGPIOInterface, GPIOInterface 
from crosslab.soa_services.webcam import WebcamService__Producer, GstTrack # pip install crosslab-soa-service-webcam

deviceUrl = 'https://api.goldi-labs.de/devices/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' # replace with your device url
deviceToken = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' # replace with your device token

# Very rudiementary python interpreter
code = ""
setRed = lambda value: None # Function to set the red light
setGreen = lambda value: None # Function to set the green light
setYellow = lambda value: None # Function to set the yellow light

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
        # We set the interface to the correct state
        interface.changeDriver('strongL')

        # We set the function to set the light
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
                
# The main function
async def main_async():
    # DeviceHandler is the main class to handle the device
    device = DeviceHandler()

    # Snippet to handle the file service ######################################
    fileService = FileService__Consumer('program')
    @fileService.on('file')
    def onFile(event: FileServiceEvent):
        global code
        code = event['content']

    device.add_service(fileService)
    ###########################################################################

    # Snippet to handle the electrical service ################################
    electricalService = ElectricalConnectionService('Ampel')
    electricalService.addInterface(ConstractableGPIOInterface(['RedLight', 'GreenLight', 'YellowLight']))
    electricalService.on("newInterface", newAmpelInterface)
    device.add_service(electricalService)
    ###########################################################################

    # Snippet to handle the webcam service ####################################
    webcamService = WebcamService__Producer(
        GstTrack("videotestsrc is-live=true pattern=ball ! videoconvert ! queue ! openh264enc "), 'webam')
    device.add_service(webcamService)
    ###########################################################################
    
    # Authentication and starting the device handler task together with the interpreter task:
    async with APIClient('https://api.goldi-labs.de') as apiClient:
        apiClient.authToken = deviceToken
        interpreterTask = asyncio.create_task(interpreter())
        deviceHandlerTask = asyncio.create_task(device.connect(deviceUrl, apiClient))
        await deviceHandlerTask

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()