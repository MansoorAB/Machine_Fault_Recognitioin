import boto3
import os
import shutil
import sys

class S3Methods:
    """
                    This class shall be used to invoke s3 operations like
                    getting files from a s3 bucket/prefix etc..,

                    Written By: Mansoor Baig
                    Version: 1.0
                    Revisions: None

                    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        self.separator = '/'  # \\' if sys.platform.startswith('win') else '/'

    def download_dir(self, bucket, prefix, local):
        """
                   Method Name: download_dir (alternate way)
                   Description: Files from s3 bucket + prefix will get saved to local directory
                   Outcome: File(s) gets saved
                   On Failure: Raise Exception

                   Written By: Mansoor Baig
                   Version: 1.0
                   Revisions: None
       """
        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket': bucket,
            'Prefix': prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = self.s3_client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            for i in contents:
                k = i.get('Key')
                if k[-1] == '/':
                    dirs.append(k)
                else:
                    keys.append(k)
            next_token = results.get('NextContinuationToken')

        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))

        for k in keys:
            k = k.replace(prefix, '')
            dest_pathname = os.path.join(local, k)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.client.download_file(bucket, k, dest_pathname)

    def get_s3_folder_data_to_local(self, bucket_name, subdir, root_dir, save_to_root=False):
        """
                   Method Name: get_s3_folder_data_to_local
                   Description: Files from specific folder in s3 bucket will get saved to local directory
                   Outcome: File(s) gets saved
                   On Failure: Raise Exception

                   Written By: Mansoor Baig
                   Version: 1.0
                   Revisions: None
       """

        try:
            prefix = subdir if subdir[-1] == '/' else subdir + '/'
            print('prefix: ', prefix)

            if save_to_root:
                shutil.rmtree(root_dir, ignore_errors=True)
                local_save_folder = root_dir
            else:
                local_save_folder = os.path.join(root_dir, prefix)

            bucket = self.s3_resource.Bucket(bucket_name)

            # downloading the folder with prefix from s3 bucket
            self.logger_object.log(self.file_object, 'Downloading data from s3 bucket: %s & prefix: %s to local '
                                                     'directory: %s' % (bucket_name, prefix, local_save_folder))

            fcount = 0
            for object in bucket.objects.filter(Prefix=prefix):
                print('object.key: ', object.key)
                if object.key == prefix:
                    os.makedirs(local_save_folder, exist_ok=True)
                    continue
                if save_to_root:
                    local_file = root_dir + self.separator + object.key.split('/')[1]
                else:
                    local_file = root_dir + self.separator + object.key
                bucket.download_file(Key=object.key, Filename=local_file)
                fcount += 1
                self.logger_object.log(self.file_object, "Downloaded file: %s to %s"
                                       % (object.key, local_file.replace(self.separator, '/')))

            self.logger_object.log(self.file_object, 'Successfully downloaded %d files to %s directory'
                                   % (fcount, local_save_folder))
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception: %s - occurred in downloading s3 bucket: %s &'
                                                     ' prefix: %s to directory: %s' % (e, bucket_name, prefix, local_save_folder))
            raise Exception()

    def get_s3_bucket_data_to_local(self, bucket_name, local):
        """
                   Method Name: download_prefix
                   Description: Files from all folder(s) in s3 bucket will get saved to local directory
                   Outcome: File(s) gets saved
                   On Failure: Raise Exception

                   Written By: Mansoor Baig
                   Version: 1.0
                   Revisions: None
       """

        try:
            bucket = self.s3_resource.Bucket(bucket_name)

            # delete existing directory if any
            if os.path.isdir(local):
                shutil.rmtree(local)
                self.logger_object.log(self.file_object, 'Folder: %s matching s3 download destination deleted.'
                                       % local)

            os.makedirs(local)
            self.logger_object.log(self.file_object, 'Folder: %s newly created, to download s3 data.' % local)

            # downloading the folder with prefix from s3 bucket
            self.logger_object.log(self.file_object, 'Downloading data from s3 bucket: %s to local '
                                                     'directory: %s' % (bucket_name, local))

            downloaded_subdir = []
            fcount = 0
            for object in bucket.objects.all():
                print(object.key)
                if object.key[-1] != '/':
                    if object.key.find('/') == -1:  # This is a file
                        local_file = local + self.separator + object.key
                        bucket.download_file(Key=object.key, Filename=local_file)
                        self.logger_object.log(self.file_object, 'Downloaded file: %s to directory: %s'
                                               % (object.key, local_file.replace(self.separator, '/')))
                        fcount += 1
                    else:
                        subdir = object.key.split('/')[0]
                        print('subdir: ', subdir)
                        if subdir not in downloaded_subdir:
                            self.get_s3_folder_data_to_local(bucket_name, subdir, local)
                            downloaded_subdir.append(subdir)
                            fcount += 1

            self.logger_object.log(self.file_object, 'Successfully downloaded %d files to %s directory'
                                   % (fcount, local))
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception: %s - occurred in downloading s3 bucket: %s '
                                                     'to directory: %s' % (e, bucket_name,  local))
            raise Exception()

    def upload_local_folder_to_s3(self, bucket_name, local, delete_local=False):

        fcount = 0
        try:
            for subdir, dirs, files in os.walk(local):
                for dir_ in dirs:
                    self.s3_client.put_object(Bucket=bucket_name, Key=dir_ + "/")
                    print('* ', dir_)
                for file in files:
                    print('** ', subdir, file)
                    if subdir == local:  # this is a file
                        local_file = os.path.join(local, file)
                        self.s3_resource.Bucket(bucket_name).upload_file(Filename=local_file, Key=file)
                        fcount += 1
                        self.logger_object.log(self.file_object, 'file: %s uploaded to s3 bucket: %s'
                                               % (file, bucket_name))
                    else:
                        sd = subdir.split(self.separator)[1]
                        print('sd: ', sd)
                        destination = sd + '/' + file
                        local_file = local + '/' + destination
                        self.s3_resource.Bucket(bucket_name).upload_file(Filename=local_file, Key=destination)
                        fcount += 1
                        self.logger_object.log(self.file_object, 'file: %s uploaded to folder: %s in s3 bucket: %s'
                                               % (file, sd, bucket_name))

            self.logger_object.log(self.file_object, 'Total file(s) uploaded: %d' % fcount)

            if delete_local:
                shutil.rmtree(local)
                self.logger_object.log(self.file_object, 'Deleted local folder: %s' % local)

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception: %s - occurred in uploading local folder: %s '
                                                     'to s3 bucket: %s' % (local, bucket_name))
            raise Exception()

    def upload_single_local_file_to_s3(self, bucket_name, local_file, grant_public_access=False):
        try:
            file = local_file.split('/')[1]
            self.s3_resource.Bucket(bucket_name).upload_file(Filename=local_file, Key=file)
            if grant_public_access:
                self.s3_resource.ObjectAcl(bucket_name, file).put(ACL='public-read')
                self.logger_object.log(self.file_object, 'public read access granted to file: %s' % file)
            self.logger_object.log(self.file_object, 'file: %s uploaded to s3 bucket: %s'
                                   % (file, bucket_name))
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception: %s - occurred while uploading file %s to '
                                                     's3 bucket %s' % (file, bucket_name))
