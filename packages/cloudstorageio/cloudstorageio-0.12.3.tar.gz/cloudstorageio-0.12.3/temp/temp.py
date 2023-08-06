from cloudstorageio import CloudInterface
from cloudstorageio.service.google_storage_interface import GoogleStorageInterface
from cloudstorageio.service.s3_interface import S3Interface

local_file_path = '/home/vahagn/dev/workspace/cognaize/cloudstorageio/cloudstorageio/tests/resources/Moon.jpg'
gs_text_file = 'gs://test-cloudstorageio/sample.txt'
s3_text_file = 's3://test-cloudstorageio/sample.txt'
ci = CloudInterface()
# ci = S3Interface()
# ci = GoogleStorageInterface()
f = ci.open(s3_text_file, 'rb')
output = f.read()
# with ci.open(s3_text_file, 'rb') as f:
#     output = f.read()
print(output)  # Prints string content of text file
