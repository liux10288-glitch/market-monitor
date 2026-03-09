import requests

# 微信推送key
sendkey = "SCT310785TyiuMic8XVy7CLH0GhULNvBej"

stocks = {
    "纳指ETF": "qqq.us",
    "半导体ETF": "smh.us",
    "恐慌指数ETF": "vxx.us"
}


def get_data(code):

    url = f"https://stooq.com/q/l/?s={code}&f=sd2t2ohlcv&h&e=json"

    r = requests.get(url, timeout=10)

    data = r.json()

    if "symbols" in data and len(data["symbols"]) > 0:

        item = data["symbols"][0]

        close = item.get("close")
        open_price = item.get("open")

        if close != "N/D" and open_price != "N/D":

            close = float(close)
            open_price = float(open_price)

            change = (close - open_price) / open_price * 100

            return close, change

    return None, None


def send_wechat(msg):

    url = f"https://sctapi.ftqq.com/{sendkey}.send"

    data = {
        "title": "市场监控提醒",
        "desp": msg
    }

    requests.post(url, data=data)


def check_market():

    qqq_price, qqq_change = get_data("qqq.us")
    smh_price, smh_change = get_data("smh.us")
    vxx_price, _ = get_data("vxx.us")

    print("市场数据")
    print("QQQ:", qqq_price, qqq_change)
    print("SMH:", smh_price, smh_change)
    print("VXX:", vxx_price)

    # 纳指强势
    if qqq_change and qqq_change > 2:

        send_wechat(f"科技股强势\nQQQ上涨 {round(qqq_change,2)}%")

    # 纳指下跌
    if qqq_change and qqq_change < -2:

        send_wechat(f"科技股走弱\nQQQ下跌 {round(qqq_change,2)}%")

    # 半导体爆发
    if smh_change and smh_change > 3:

        send_wechat(f"半导体行情启动\nSMH上涨 {round(smh_change,2)}%")

    # 半导体下跌
    if smh_change and smh_change < -3:

        send_wechat(f"半导体走弱\nSMH下跌 {round(smh_change,2)}%")

    # 恐慌指数
    if vxx_price and vxx_price > 25:

        send_wechat(f"市场恐慌上升\nVIX ETF {vxx_price}")


if __name__ == "__main__":

    check_market()