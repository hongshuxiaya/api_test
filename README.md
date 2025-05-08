**首先安装本项目所需的依赖库，cmd命令为：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r E:\api_test_frame\requirements.txt
其中：E:\api_test_frame路径替换自己项目的磁盘路径。**

# **接口自动化测试框架规则说明**

**1、测试用例yaml文件检查必要的四个一级关键字：name，base_url，request，validate。**

**2、测试用例yaml文件在request关键字下包含二个二级关键字：method，url。**

**3、传参方式：在request一级关键字下，通过二级关键字参数。**

如果是get请求，通过params传参。

如果是post请求:

    传json格式，通过json关键字传参。
    传表单格式，通过data关键字传参。
    传文件格式，通过files关键字传参，如：
    files：
        media：./logo.png

**4、如果需要做接口关联的话，那么必须使用一级关键字: extract。**

提取：

    如:jsonpath提取方式：
    extract:
        expires_in: $.expires_in

    如:正则表达式提取方式：
    extract:
        access_token: '"access_token":"(.*?)"'

取值：

    如测试用例yaml文件中，使用get_extract_data函数获取access_token值：
    ${get_extract_data(access_token)}

**5、热加载，当测试用例文件yaml中需要使用动态参数时，那么可以在debug_talk.py文件中写方法来调用。**

  注意：传参时，需要什么类型的数据，需要先做强制转换。int(mix),int(max)，如：

    创建获取随机数函数：
    def get_random_number(self,mix,max):
        return random.randint(int(mix),int(max))
    测试用例yaml文件中，使用热加载方式调取函数取值：
    ${get_random_number(100000,999999)}

**6、目前框架暂时只支持两种断言方式：分别是equals(相等)和contains(包含)断言方式。**

如：
 
    validate:
       - equals: {status_code: 200}
       - contains: access_token

**7、数据驱动使用一级关键字parameterize实现。**

如：yaml中写法：

  parameterize:

    - ['name','appid','secret','grant_type','assert_str']
    - ['获取access_token统一鉴权码','wx8cbefbfc3b8c2f3b','4fa4582bf6b362742f079a3b7709ccad','client_credential','access_token']
    - ['appid必填项检查',"",'4fa4582bf6b362742f079a3b7709ccad','client_credential','errcode']
    - ['secret必填项检查','wx8cbefbfc3b8c2f3b',"",'client_credential','errcode']
ddt写法：

    $ddt{name}:引用parameterize中的参数name。

**8、日志监控，异常处理，以及基础路径的设置。**

**9、框架使用说明。**

各目录含义：

    commons：工具类。
    config：配置文件，config.yaml：配置基础url和log日志；extract.yaml：接口提取字段存放文件。
    docs：接口文档说明、笔记。
    data：mock接口数据。
    logs：日志文件。
    reports：allure报告、html报告。
    server：一个电商mock服务接口，启动后，可运行shop下的测试用例。
    testcases：测试用例。php：论坛的网站；takeaway：外卖项目接口；user：码尚商城登录加密的案例；weixin：微信公众号平台；shop：电商项目。
    conftest：pytest配置全局文件。
    environment.xml：allure报告环境设置。
    categories.json：allure报告categories设置。
    pytest.ini：pytest运行集。
    requiremens.txt:框架所需的第三方库。
    run.py：框架运行入口。

testcases中写了几个案例：

    php论坛的网站：论坛首页、sign签名。
    takeaway：外卖项目接口：注册、登录、增删改查。
    码尚商城：用户登录base64、md5、rsa加密。
    微信公众号：登录、标签的增删改查和文件上传。其中登录做了3个参数化：获取access_token统一鉴权码、appid必填项检查、secret必填项检查。
    shop：电商项目，需要启动服务。

**10、数据库、jenkins、接口地址、钉钉和QQ邮箱的个人数据设置，请使用自己的账号，都在config/config.yaml中配置。**

dingding_robot.py文件中钉钉：密钥secret、钉钉机器人的Webhook地址。

send_mail.py文件中QQ邮箱：邮箱账号、授权码。

**11、Mock模拟接口场景，如果没有实际项目，则可以直接运行server/flask_service.py文件，然后再去运行run.py。**

**12、测试报告。**

allure报告和html报告二种，可在config/config.yaml中选择报告类型，pytest.ini中修改运行。

allure报告Categories：分类（测试用例结果的分类），默认情况下，有两类缺陷：

    Product defects：产品缺陷（测试结果：failed）。
    Test defects：测试缺陷（测试结果：error/broken）。

categories.json的参数解释：

    name：分类名称。
    
    matchedStatuses：测试用例的运行状态，默认[“failed”, “broken”, “passed”, “skipped”, “unknown”]。
    
    messageRegex：测试用例运行的错误信息，默认是 .* ，是通过正则去匹配的。
    
    traceRegex：测试用例运行的错误堆栈信息，默认是 .* ，是通过正则去匹配的。
