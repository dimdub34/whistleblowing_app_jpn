def seconds_to_minutes(seconds, return_string=True):
    minutes = seconds // 60
    reste = seconds % 60
    if return_string:
        if minutes == 0:
            txt = f"{reste} 秒"
        else:
            txt = f"{minutes} 分"
            if reste:
                txt += f" {reste} 秒"
        return txt
    else:
        return minutes, reste
