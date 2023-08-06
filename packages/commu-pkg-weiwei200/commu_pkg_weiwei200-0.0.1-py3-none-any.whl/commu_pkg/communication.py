#coding=utf-8

import socket
import threading
import uuid
import datetime
import io
import urllib
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#回调函数示例1
class CallBackObject:
    def callback_func(self, eventArgs):

        pass

#回调函数示例2
def callback_func(eventArgs):

    pass

class TcpServer:
    #全局变量
    ip = None
    port = None
    function = None

    def __init__(self):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        pass

    def start(self, ip='127.0.0.1', port=10000, count=1000):
        TcpServer.ip = ip
        TcpServer.port = port

        self.m_socket.bind((ip, port))

        self.m_socket.listen(count)

        param_args = []
        param_args.append(3700*10000)

        param_kwargs = {}
        param_kwargs.__setitem__("DLT", "37000000")
        param_kwargs.__setitem__("CPRQ", "20190501")

        thd = threading.Thread(target=self.__work, name="listen", args=param_args, kwargs=param_kwargs)
        thd.setDaemon(True)
        thd.start()

        pass

    def __work(self, *args, **kwargs):
        temp1 = args[0]
        temp2 = kwargs["DLT"]

        self.check_label = True

        while self.check_label == True:
            #接收到的网络连接
            channel, addr_port = self.m_socket.accept()

            chat = ChatServer(channel, addr_port, self.m_socket)
            pass

        pass


    def async_send2c(self, channel, data):

        len_data = len(data)
        len_str = self.__int2string(len_data)
        new_data = len_str + data

        channel.send(new_data)

        pass

    def __int2string(self, count):
        str = '%04d' %count
        return str

    #注册接收数据事件函数/回调函数
    def add_eventhandler(self, function):
        TcpServer.function = function
        pass

    def remove_eventhandler(self):
        TcpServer.function = None
        pass

class ChatServer:
    #全局变量
    Map = {}

    def __init__(self, channel, addr, m_socket):

        self.Id = str(uuid.uuid1())

        self.channel = channel

        self.addr = addr #(ip, port)

        self.m_socket = m_socket

        self.state = 1

        ChatServer.Map.__setitem__(self.Id, self)

        thd = threading.Thread(target=self.__receivemessage, name="chatserver", args=(), kwargs={})
        thd.setDaemon(True)
        thd.start()

        pass

    def __receivemessage(self):
        check_receive = True

        try:
            while check_receive == True:

                bol = True

                recv_count_str = self.channel.recv(4)

                recv_count = int(recv_count_str)

                shengyu_count = recv_count

                recv_str = ''

                check = True

                while check:
                    temp_str = self.channel.recv(shengyu_count)

                    recv_str += temp_str

                    temp_count = len(temp_str)

                    shengyu_count = shengyu_count - temp_count

                    if shengyu_count == 0:
                        check = False

                        print "receive_message:" + recv_str

                        event_args = TcpSv_EventArgs(self, recv_str)

                        temp_args = []
                        temp_args.append(event_args)

                        thd = threading.Thread(target=self.fire_event, name='fire', args=temp_args, kwargs={})
                        thd.setDaemon(True)
                        thd.start()
                        pass

                pass
            pass
        except socket.error, e:
            print e
            self.state = 0
        except Exception, e:
            print e
            self.state = 0
        finally:
            if self.state == 0:
                check_receive = False
                self.channel.close()
        pass

    #调用回调函数，通知外界
    def fire_event(self, *args, **kwargs):
        temp = args[0]

        if TcpServer.function != None:
            TcpServer.function(temp)

        pass

#TCP服务端回调函数的参数
class TcpSv_EventArgs:
    def __init__(self, chatserver, data):
        self.chatserver = chatserver

        self.data = data
        pass

#TCP客户端回调函数的参数
class TcpCl_EventArgs:
    def __init__(self, data):
        self.data = data
        pass

class TcpClient:
    def __init__(self):

        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ''
        self.port = 0
        self.function = None

        self.state = 1

        self.check_label = True

        pass

    def connect(self, ip, port):

        self.ip = ip
        self.port = port

        self.m_socket.connect((ip, port))

        pass

    #同步---请求/响应形式
    def send(self, data=""):

        count = len(data)

        len_str = self.__int2string(count)

        buf = len_str + data

        self.m_socket.send(buf)

        recv_count_str = self.m_socket.recv(4)

        recv_count = int(recv_count_str)

        shengyu_count = recv_count

        recv_str = ''

        check = True

        while check == True:
            temp_str = self.m_socket.recv(shengyu_count)

            recv_str += temp_str

            temp_count = len(temp_str)

            shengyu_count = shengyu_count - temp_count

            if shengyu_count == 0:
                check = False

        result = recv_str

        return result

    #同步发送---数据报形式
    def async_send(self, data=""):

        count = len(data)

        len_str = self.__int2string(count)

        buf = len_str + data

        self.m_socket.send(buf)

        pass

    #异步接收---数据报形式
    def async_receive(self, function):

        self.function = function

        thd = threading.Thread(target=self.__receive_work, name="async_receive_work")
        thd.setDaemon(True)
        thd.start()

        pass

    def __receive_work(self):

        check_receive = True

        try:
            while check_receive == True:

                bol = True

                recv_count_str = self.m_socket.recv(4)

                recv_count = int(recv_count_str)

                shengyu_count = recv_count

                recv_str = ''

                check = True

                while check:
                    temp_str = self.m_socket.recv(shengyu_count)

                    recv_str += temp_str

                    temp_count = len(temp_str)

                    shengyu_count = shengyu_count - temp_count

                    if shengyu_count == 0:
                        check = False
                        pass

                    print "receive_message:" + recv_str

                    event_args = TcpCl_EventArgs(recv_str)

                    temp_args = []
                    temp_args.append(event_args)

                    thd = threading.Thread(target=self.fire_event, name='fire', args=temp_args, kwargs={})
                    thd.setDaemon(True)
                    thd.start()

                pass
            pass
        except socket.error, e:
            print e
            self.state = 0
        except Exception, e:
            print e
            self.state = 0
        finally:
            if self.state == 0:
                self.m_socket.close()

        pass

    # 调用回调函数，通知外界
    def fire_event(self, *args, **kwargs):
        temp = args[0]

        if TcpServer.function != None:
            self.function(temp)

        pass

    def __int2string(self, count):
        str = '%04d' %count
        return str


class HttpSv_EventArgs:
    function = None

    def __init__(self, http_obj, http_info):
        self.Http_object = http_obj
        self.Http_info = http_info

    pass

class HttpProtocols:
    Http = 0
    Https = 1

class HttpServer:
    def __init__(self, http_protocols=HttpProtocols.Http):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.http_protocols = http_protocols



        pass

    def start(self, ip='127.0.0.1', port=80):

        accept_count = 100

        self.m_socket.bind((ip, port))
        self.m_socket.listen(accept_count)

        thd = threading.Thread(target=self.__listen)
        thd.setDaemon(True)
        thd.start()

        pass

    def __listen(self, *args, **kwargs):

        self._isrunning = True

        while self._isrunning == True:

            channel, addr_port = self.m_socket.accept()

            http_obj = HttpObject(channel, addr_port)

            pass

        pass

    def stop(self):

        self.m_socket.close()

        pass

    # 注册接收数据事件函数/回调函数
    def add_eventhandler(self, function):
        HttpServer.function = function
        pass

    def remove_eventhandler(self):
        HttpServer.function = None
        pass


class HttpObject:
    def __init__(self, channel, addr_port):

        self.channel = channel
        #套接字设置为非阻塞，等于
        #self.channel.settimeout(0.0)
        #self.channel.setblocking(False)

        #套接字设置为阻塞60秒
        #self.channel.settimeout(5)

        self.addr_port = addr_port

        thd = threading.Thread(target=self.__main_work)
        thd.setDaemon(True)
        thd.start()

        pass

    def send(self, data):

        self.channel.send(data)

        pass

    def __main_work(self):

        buf = io.BytesIO()

        max_count = 1024 * 64

        check = True

        recv_data = ""

        while check:
            try:
                temp = self.channel.recv(max_count)

                recv_data += temp

                _is_contains = "\r\n\r\n" in recv_data

                body_str = None

                if _is_contains == True:
                    #check = False
                    #处理字符串
                    end_index = recv_data.find("\r\n\r\n")

                    tmp = recv_data[0:(end_index+4)]

                    head_str = tmp

                    #解析消息头
                    http_info = self.__get_http_head(head_str)

                    #根据消息头处理消息体

                    body_contains = True
                    length_body = 0

                    try:
                        length_body_str = http_info.Headers["Content-Length"]

                        length_body = int(length_body_str)

                        pass
                    except Exception, ex:
                        body_contains = False
                        pass
                    finally:
                        pass

                    if body_contains == True:
                        #存在长度，表示有消息体，从已接收到的信息的 \r\n\r\n+4之后开始算起；
                        body_str = recv_data[end_index+4:]

                        body_recv_len = len(body_str)

                        shengyu_count = length_body - body_recv_len

                        while body_recv_len != length_body:
                            temp_str = self.channel.recv(shengyu_count)

                            body_str += temp_str

                            temp_count = len(temp_str)

                            shengyu_count = shengyu_count - temp_count

                            body_recv_len = body_recv_len + temp_count

                            pass

                        pass
                    else:

                        chunk_contains = True

                        #判断字典中是否存在Transfer-Encoding
                        try:

                            chunk_ = http_info.Headers["Transfer-Encoding"]

                            if chunk_ != "chunked":
                                chunk_contains = False

                            pass
                        except Exception, ex:
                            chunk_contains = False
                            pass
                        finally:
                            pass

                        #如果有分段传输，进行处理
                        if chunk_contains == True:

                            #分块传输，读到    0\r\n\r\n为止
                            body_temp_str = recv_data[end_index + 4:]

                            bol = "\r\n0\r\n\r\n" in body_temp_str

                            chunk_check = True

                            buf = io.BytesIO()

                            buf.write(body_temp_str.encode("utf-8"))

                            if bol == True:
                                chunk_check = False

                            while chunk_check == True:

                                body_temp_str = self.channel.recv(max_count)

                                bol = "\r\n0\r\n\r\n" in body_temp_str

                                if bol == True:
                                    chunk_check = False

                                    tmp_index = body_temp_str.find("\r\n0\r\n\r\n")

                                    tmp_str = body_temp_str[:(tmp_index+7)]

                                    body_temp_str = tmp_str

                                    pass

                                buf.write(body_temp_str.encode("utf-8"))

                            pass

                            body_str = buf.getvalue()

                        pass

                    #接收完成数据
                    http_info.Body = body_str

                    pass

            except Exception, ex:
                print ex

                #异常则进行关闭Socket，通知外界
                self.channel.close()

            finally:
                print recv_data
                pass

            #接收完数据，通知外界
            temp_args = []
            temp_args.append(http_info)

            thd = threading.Thread(target=self.fire_event, name='fire', args=temp_args, kwargs={})
            thd.setDaemon(True)
            thd.start()


            #通过判断是否是keep-alive保持连接
            keep_alive_check = True
            try:
                keep_alive_str = http_info.Headers["Connection"]

                if keep_alive_str != "keep-alive":
                    check = False
                    self.channel.close()

            except Exception, ex:
                check = False
                self.channel.close()
            finally:
                pass

            pass

        pass

    def __get_http_head(self, data):

        http_info = HttpInfo()

        #接收到的数据按行分组
        lines = data.splitlines()

        #处理请求行
        fst_str = lines[0]
        fst_list = fst_str.split(" ")

        http_info.type = fst_list[0]
        http_info.Protocol = fst_list[2]

        if http_info.type == "GET":
            #处理请求行上的参数
            tmp = fst_list[1]
            tmp_lst = tmp.split("?")

            http_info.url = tmp_lst[0]

            params_str = tmp_lst[1]
            params_str_lst = params_str.split("&")

            for param_tmp in params_str_lst:

                param_objs = param_tmp.split("=")
                param_key = param_objs[0]
                param_value = param_objs[1]

                http_info.Params.__setitem__(param_key, param_value)

                pass

            pass
        else:

            http_info.url = fst_list[1]

            pass

        #处理请求头
        i = 1

        lines_count = len(lines)

        while i < lines_count:

            line_str = lines[i]

            head_check = ":" in line_str

            if head_check == True:

               line_lst = line_str.split(":")
               key = line_lst[0]
               value_tmp = line_lst[1]
               value = value_tmp[1:]

               http_info.Headers[key] = value

               pass


            i = i + 1

            pass

        return http_info
        pass

    def fire_event(self, *args, **kwargs):

        temp = args[0]

        event_args = HttpSv_EventArgs(self, temp)

        if HttpServer.function != None:
            HttpServer.function(event_args)

        pass

    '''
    def __get_http_info(self, data):

        # 把接收到的数据按行分组
        lines = data.splitlines()

        fst_str = lines[0]
        fst_list = fst_str.split(" ")
        type_str = fst_list[0]

        type_data = type_str.upper()

        lines_count = len(lines)

        http_info = HttpInfo()
        http_info.info_data = data

        if type_data == "OPTIONS":
            http_info.type = "OPTIONS"

            i = 1

            check = True

            while check:

                item_str = lines[i]

                bol = ":" in item_str
                bol_body = False

                if bol == True:

                    if bol_body == False:

                        item = item_str.split(":", 1)
                        item_key = item[0]
                        item_value = item[1]

                        http_info.Headers[item_key] = item_value
                        pass
                    else:
                        http_info.Body += item_str
                    pass
                else:
                    if item_str == "":
                        #查找到""字符串，意味着后面的是POST消息体
                        bol_body = True
                    pass

                i = i + 1
                if i == lines_count:
                    check = False

                pass

            pass
        elif type_data == "GET":
            http_info.type = "GET"

            body = fst_list[1]
            http_info.Body = body[1:]

            i = 2

            check = True

            while check:

                item_str = lines[i]

                bol = ":" in item_str

                if bol == True:
                    item = item_str.split(":", 1)
                    item_key = item[0]
                    item_value = item[1]

                    http_info.Headers[item_key] = item_value
                    pass

                i = i + 1
                if i == lines_count:
                    check = False

                pass

            pass
        elif type_data == "POST":
            http_info.type = "POST"

            i = 1

            check = True

            while check:

                item_str = lines[i]

                bol = ":" in item_str
                bol_body = False

                if bol == True:

                    if bol_body == False:

                        item = item_str.split(":", 1)
                        item_key = item[0]
                        item_value = item[1]

                        http_info.Headers[item_key] = item_value
                        pass
                    else:
                        http_info.Body += item_str
                    pass
                else:
                    if item_str == "":
                        # 查找到""字符串，意味着后面的是POST消息体
                        bol_body = True
                    pass

                i = i + 1
                if i == lines_count:
                    check = False

                pass
            pass

        return http_info

        pass
    '''

    '''
    def __work(self, http_info):

        if http_info.type == "OPTIONS":

            self.__options_work(http_info)

            pass
        elif http_info.type == "GET":

            pass
        elif http_info.type == "POST":

            pass

        pass
    '''

    '''
    #返回应答信息
    def __options_response_work(self, http_info):

        response_str = "HTTP/1.1 200 OK" + '\n'

        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        date = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        data_str = str(date)

        response_str += "Date:" + data_str + '\n'
        response_str += "Server: Dam/1.0.01 (Unix)"+'\n'
        response_str += "Access-Control-Allow-Orgin:" + "192.168.0.163:8080" + '\n'
        response_str += "Access-Control-Allow-Methods:" + "GET, POST, PUT" + '\n'
        response_str += "Access-Control-Request-Headers:" + "content-type" + '\n'
        response_str += "Content-Type:text/html; charset=utf-8" + '\n'
        response_str += "Content-Encoding: gzip" + '\n'
        response_str += "Connection:"+ "Keep-Alive" + '\n'

        self.channel.send(response_str)

        pass
        '''

    pass

class HttpInfo:
    def __init__(self):

        self.type = None
        self.url = None
        self.type_str = None
        self.Headers = {}
        self.Body = ""
        self.Params = {}
        self.Protocol = None

        self.info_data = ""

        pass

class HttpClient:
    def __init__(self):

        pass




if __name__ == "__main__":
    http_server = HttpServer()
    http_server.start("192.168.0.164", 8080)

    while True:
        threading._sleep(500)