import base64, zipfile, io
from fastapi import UploadFile
from app.connectors.kafka.interface.faststream_producer import FastStreamKafkaProducer

class FileUploader:
    def __init__(self, producer: FastStreamKafkaProducer):
        self.producer = producer

    async def send_file_base64(self, topic: str, file: UploadFile):
        await self.producer.broker.start()
        try:
            if file.content_type == "application/zip":
                contents = await file.read()
                with zipfile.ZipFile(io.BytesIO(contents)) as zf:
                    for name in zf.namelist():
                        with zf.open(name) as f:
                            data = f.read()
                            msg = {
                                "filename": name,
                                "content_type": "application/octet-stream",
                                "data": base64.b64encode(data).decode(),
                                "meta": {}
                            }
                            await self.producer.send(topic, msg)
            else:
                data = await file.read()
                msg = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "data": base64.b64encode(data).decode(),
                    "meta": {}
                }
                await self.producer.send(topic, msg)
        finally:
            await self.producer.broker.close()

    async def send_file_binary(self, topic: str, file: UploadFile):
        await self.producer.broker.start()
        try:
            if file.content_type == "application/zip":
                contents = await file.read()
                with zipfile.ZipFile(io.BytesIO(contents)) as zf:
                    for name in zf.namelist():
                        with zf.open(name) as f:
                            data = f.read()
                            msg = {
                                "filename": name,
                                "content_type": "application/octet-stream",
                                "data": data.hex(),
                                "meta": {}
                            }
                            await self.producer.send(topic, msg)
            else:
                data = await file.read()
                msg = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "data": data.hex(),
                    "meta": {}
                }
                await self.producer.send(topic, msg)
        finally:
            await self.producer.broker.close()
