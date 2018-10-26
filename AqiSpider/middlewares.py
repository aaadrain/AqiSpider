# coding: utf-8
import time
import scrapy
from selenium import webdriver
from retrying import retry
class SeleniumDownloaderMiddleware(object):
    def __init__(self):

        # self.driver = webdriver.Chrome()   # 有界面的

        # 无界面(对内存占有率小,效率更高)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=self.options)

    # 1.(理想状态) self.driver.find_element_by_xpath("//tbody/tr[2]/td[1]") 查找页面内容是否出现异常,如果没有异常出现.则 retry 和 try 都不工作,方法正常执行结束,继续执行后面的代码.

    # 2.(不理想状态) self.driver.find_element_by_xpath("//tbody/tr[2]/td[1]")没有找到页面内容,抛出了异常,让 try 工作,并在 except 同过 raise 抛出异常让 retry 工作,继续充实代码执行,如果20次重试次数内找到页面内容了,方法正常执行结束,继续执行后续代码

    # 3.(无法正常处理页面状态) 如果 retry 在20次重试次数内都没有找到内容,则 retry 不再工作, raise 的异常将抛出给调用的地方,在后续代码中处理异常


    @retry(stop_max_attempt_number=20,wait_fixed=200)
    def retry_load_page(self,request,spider): # spider 里面有 url
        try:
            self.driver.find_element_by_xpath("//tbody/tr[2]/td[1]")
        except:
            spider.logger.info("Retry load page [{}] <{}>".format(self.count,request.url))
            self.count+=1
            # 这边抛出异常是给 retry 进行判断继续尝试的
            raise Exception("<{}> page load failed".format(request.url))

    def process_request(self,request,spider):
        if "daydata" in request.url or "monthdata" in request.url:
            self.count = 1
            # print("[INFO]url:<{}>".format(request.url))
            self.driver.get(request.url)
            # 显示等待 固定时间
            #time.sleep(2)

            try:  # 如果这个 retry 20次都尝试完了.这个页面还是没有东西出来
            # 那么则返回 request 给调度器,下一次在进行尝试
                # 隐式等待
                self.retry_load_page(request,spider)
                html = self.driver.page_source
                # 构建自定义的相应对象(必须的属性 url,body,encoding,request)
                response = scrapy.http.HtmlResponse(
                    url=self.driver.current_url,
                    body=html.encode("utf-8"),
                    encoding='utf-8',
                    request=request
                    )
                # 返回一个自定义响应对象,引擎会认为这是下载器返回的响应,默认交给 spider 解析
                # 返回 none, 则该请求继续交给下载器,返回 Request, 则该请求重新进入调度器执行重新发送)
                return response
            except Exception as e:
                spider.logger.info(e)
                # 返回 request 请求到调度器中
                return request 
