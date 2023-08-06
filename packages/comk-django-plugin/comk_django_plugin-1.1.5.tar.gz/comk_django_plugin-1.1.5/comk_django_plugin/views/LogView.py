from django.conf import settings
from django.http import StreamingHttpResponse
from django.views import View


class GetLog(View):
    '''
    获取日志（城市分发）
    '''

    def get(self, request, log_name):
        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        BASE_DIR = settings.BASE_DIR
        the_file_name = "{}/log/{}.log".format(BASE_DIR, log_name)
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}.log"'.format(log_name)
        return response
