from http import HTTPStatus
from ogero.types import LoginResponse, ErrorResponse

json_headers = {"content-type": "application/json"}
html_headers = {"content-type": "text/html"}

MOCK_SESSION_ID = "session_id1"


def successful_login_response():
    data: LoginResponse = {"SessionID": MOCK_SESSION_ID}
    return data, HTTPStatus.OK, json_headers


def failed_login_response():
    data: ErrorResponse = {
        "error": {"code": "2002", "message": "Wrong username/password combination"}
    }
    return data, HTTPStatus.BAD_REQUEST, json_headers


def unauthorized_response():
    data: str = '<script language="javascript">window.location="login.logout.php?error=You are required to login to access this section";</script>'
    return data, HTTPStatus.OK, html_headers


def dashboard_response():
    data: str = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>My Ogero - Dashboard</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  </head>
  <body>
    <div id="fb-root"></div>
    <div class="MyOgeroDashboardContainer">
      <div class="MyOgeroDashboard">
        <div class="MyOgeroDashboardSection3" style="padding: 0px;">
          im here
          <div class="MyOgeroDashboardSection2NumberChangeContainer">
            <div class="MyOgeroDashboardSection2NumberChange">
              <div>Account</div>
              <select name="changnumber" id="changnumber">
                <option value="xxxxxxxx" value2="Lxxxxxx" selected> Lxxxxxx / xx xxxxxx </option>
              </select>
              <i class="fa fa-chevron-down" aria-hidden="true"></i>
              <a href="enroll.php?&AppRequest&Select=enrollanumber" class="BackgroundGradient"></a>
            </div>
          </div>
          <div class="sep" style="height: 10px;"></div>
          <div class="MyOgeroDashboardSection2Services">
            <div>Telephone Number<span>xx xxxxxx</span></div>
          </div>
          <div align="center" style="font-size: 16px;">
            Welcome <br />
            <b style="font-weight: 700;">John Doe </b>
          </div>
          <div class="MyOgeroDashboardSection2Container">
            <div class="MyOgeroDashboardSection2Bill">
              <div class="BackgroundGradient">
                <section>100,000<span>L.L.</span><a href="javascript:;">pay bill now</a></section>
              </div>
              <b>Bills Until</b>July 2022
            </div>
          </div>
          <form name="billpaymentform" id="billpaymentform" method="post" action="payment.to.php">
            <input type="hidden" name="procedure" value="phonebill" />
            <input type="hidden" name="srvline" value="xxxxxxx" />
            <input type="hidden" name="number" value="xxxxxxx" />
          </form>
          <div class="sep"></div>
        </div>
      </div>
    </div>
  </body>
</html>
    """
    return data, HTTPStatus.OK, html_headers

def consumption_response():
  data: str = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Ogero - My Consumption</title>
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-16x16.png" sizes="16x16" />
    <meta name="viewport" content="initial-scale=1, maximum-scale=1" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  </head>
  <body>
    <div id="fb-root"></div>
    <div class="MyOgeroDashboardContainer">
      <div class="MyOgeroDashboard" data-aos="fade-right">
        <div class="BillNumberChange" data-aos="fade-right" data-aos-delay="0">
          <div class="MyOgeroDashboardSection2NumberChangeContainer">
            <div class="MyOgeroDashboardSection2NumberChange">
              <div>Internet Account</div>
              <select name="changnumber">
                <option value="L454714" selected>Lxxxxxx [ Phone #: xx xxxxxx ] </option>
              </select>
              <i class="fa fa-chevron-down" aria-hidden="true"></i>
              <a class="BackgroundGradient"></a>
            </div>
          </div>
        </div>
        <div class="MyOgeroDashboardSection3" data-aos="fade-right" data-aos-delay="200">
          <div class="MyOgeroDashboardSection1Name">My Consumption</div>
          <div class="sep"></div>
          <div class="MyConsumptionRight"></div>
          <div class="MyConsumptionLeft">
            <div class="MyConsumptionGrid"><span>Connection Speed</span><span> <= 50 Mbps </span></div>
            <div class="MyConsumptionGrid"><span>Quota</span><span>Unlimited GB</span></div>
            <div class="MyConsumptionGrid"><span>Upload</span><span> 12.0 GB</span></div>
            <div class="MyConsumptionGrid"><span>Download</span><span> 143.4 GB</span></div>
            <div class="MyConsumptionGrid"><span>Total Consumption</span><span> 155.4 GB</span></div>
            <div class="MyConsumptionGrid"><span>Extra Consumption</span><span>0</span></div>
            <div class="MyConsumptionGrid"><span>Consumption Until</span><span>SEPTEMBER 15,2022 17:03</span></div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
  """
  return data, HTTPStatus.OK, html_headers

def bill_response():
  data: str = """
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>Ogero - My Bills</title>
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-16x16.png" sizes="16x16" />
    <meta name="viewport" content="initial-scale=1, maximum-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

<body>
    <div id="fb-root"></div>

    <div class="MyOgeroDashboardContainer">
        <div class="MyOgeroDashboard">
            <div class="BillNumberChange" data-aos="fade-right" data-aos-delay="0">
                <div class="MyOgeroDashboardSection2NumberChangeContainer">
                    <div class="MyOgeroDashboardSection2NumberChange">
                        <div>Phone Number</div>
                        <select name="changnumber">
                            <option value="xxxxxxxx" selected>xx xxxxxx [ DSL # Lxxxxxx ] </option>
                        </select>
                        <i class="fa fa-chevron-down" aria-hidden="true"></i>
                        <a class="BackgroundGradient"></a>
                    </div>

                </div>
            </div>
            <div class="MyOgeroDashboardSection3" data-aos="fade-right" data-aos-delay="200">
                <div class="BillOutstandingSection1">Your Outstanding bills value: <span>250,000 L.L.</span></div>
                <div class="BillOutstandingSection2 BackgroundGradient">
                    <div class="ButtonRounded BackgroundGradient">
                        <a href="javascript:;" target="_blank">Pay Now</a></div>
                </div>
                <div class="sep"></div>
                <form name="billpaymentform" id="billpaymentform" method="post" action="payment.to.php">
                    <input type="hidden" name="procedure" value="phonebill">
                    <input type="hidden" name="srvline" value="xxxxxxx">
                    <input type="hidden" name="number" value="xxxxxxxx">
                </form>
                <div class="MyOgeroDashboardSection1Name">My Bills for <span>xx xxxxxx</span></div>
                <div class="sep"></div>
                <div class="sep"></div>
                <table class="BillTable" cellspacing="0" cellpadding="10" width="100%">
                    <tr>
                        <th></th>
                        <th>Bill Value</th>
                        <th>Payment Status</th>
                        <th>Operations</th>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jul</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">200,000 L.L.</div>
                        </td>
                        <td>Not paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jun</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">50,000 L.L.</div>
                        </td>
                        <td>Not paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>May</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">40,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Apr</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">50,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Mar</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">60,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jan</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">44,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <div class="BillMenuMobile" id="BillMenuMobile_0">
        <div class="BillMenuMobileClose" ><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_1">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_2">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_3">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_4">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_5">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
</body>

</html>
  """
  return data, HTTPStatus.OK, html_headers

def bill_response_no_outstanding_bill():
  data: str = """
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>Ogero - My Bills</title>
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="https://ogero.gov.lb/img/favicon-16x16.png" sizes="16x16" />
    <meta name="viewport" content="initial-scale=1, maximum-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

<body>
    <div id="fb-root"></div>

    <div class="MyOgeroDashboardContainer">
        <div class="MyOgeroDashboard">
            <div class="BillNumberChange" data-aos="fade-right" data-aos-delay="0">
                <div class="MyOgeroDashboardSection2NumberChangeContainer">
                    <div class="MyOgeroDashboardSection2NumberChange">
                        <div>Phone Number</div>
                        <select name="changnumber">
                            <option value="xxxxxxxx" selected>xx xxxxxx [ DSL # Lxxxxxx ] </option>
                        </select>
                        <i class="fa fa-chevron-down" aria-hidden="true"></i>
                        <a class="BackgroundGradient"></a>
                    </div>

                </div>
            </div>
            <div class="MyOgeroDashboardSection3" data-aos="fade-right" data-aos-delay="200">
                <div class="MyOgeroDashboardSection1Name">My Bills for <span>xx xxxxxx</span></div>
                <div class="sep"></div>
                <div class="sep"></div>
                <table class="BillTable" cellspacing="0" cellpadding="10" width="100%">
                    <tr>
                        <th></th>
                        <th>Bill Value</th>
                        <th>Payment Status</th>
                        <th>Operations</th>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jul</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">200,000 L.L.</div>
                        </td>
                        <td>Not paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jun</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">50,000 L.L.</div>
                        </td>
                        <td>Not paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>May</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">40,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Apr</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">50,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Mar</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">60,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="BillDate BackgroundGradient">
                                <div>Jan</div><span>2022</span>
                            </div>
                        </td>
                        <td>
                            <div class="BillAmount">44,000 L.L.</div>
                        </td>
                        <td>Paid</td>
                        <td>
                            <div class="BillMenuDesktop">
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed Invoice</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a> |
                                <a class="BillLink" target="_blank" data-fancybox="iframe" data-type="iframe">
                                    <i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
                            </div>
                            <a href="javascript:;" class="BillMenuMobileLink BackgroundGradient">
                                <i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <div class="BillMenuMobile" id="BillMenuMobile_0">
        <div class="BillMenuMobileClose" ><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_1">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_2">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_3">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_4">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
    <div class="BillMenuMobile" id="BillMenuMobile_5">
        <div class="BillMenuMobileClose"><i class="fa fa-times" aria-hidden="true"></i></div>
        <a target="_blank"><i class="fas fa-file-invoice-dollar" aria-hidden="true"></i> Detailed invoice</a>
        <a target="_blank"><i class="fa fa-mobile" aria-hidden="true"></i> Outgoing GSM Calls</a>
        <a target="_blank"><i class="fa fa-phone" aria-hidden="true"></i> Outgoing International Calls</a>
    </div>
</body>

</html>
  """
  return data, HTTPStatus.OK, html_headers