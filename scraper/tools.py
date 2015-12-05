import json, shutil, os


def loadJsonFile(pathToJson):
    with open(pathToJson) as data_file:
        return json.loads( data_file.read() )

def saveImage(self, r, filename):
    """
        save downaloded image
    """
    FULL_PATH = os.path.join(self.OUTPUT_DIR, filename )

    with open(FULL_PATH, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
