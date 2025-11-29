from contextlib import asynccontextmanager
from io import BytesIO

from aiobotocore.session import get_session


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            region_name: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region_name
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_fileobj(self, file_data: bytes, object_name: str):
        file_bytes = BytesIO(file_data)
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_bytes
            )

    # async def upload_file(
    #         self,
    #         file_path: str,
    # ):
    #     object_name = file_path.split("/")[-1]
    #     async with self.get_client() as client:
    #         with open(file_path, "rb") as file:
    #             await client.put_object(Bucket=self.bucket_name, Key=object_name, Body=file)

    async def download_file(self, file_path: str):
        async with self.get_client() as client:
            resp = await client.get_object(Bucket=self.bucket_name, Key=file_path)
            async with resp['Body'] as stream:
                load_data = await stream.read()
        return load_data

    async def delete_file(self, file_path: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_path)
