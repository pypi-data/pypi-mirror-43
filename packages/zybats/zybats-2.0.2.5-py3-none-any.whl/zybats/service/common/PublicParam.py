import time

def init_PublicPara(request):
	request['data']['_t_'] =  int(time.time())
	request['data']['channel'] = 'appstore'
	request['data']['cuid'] = 'b53f7444e8c9cf2a08f11f5dda35aabe129af643'
	request['data']['device'] = 'iPhone11,8'
	request['data']['iOSVersion'] = '12.1.2'
	request['data']['nt'] = 'wifi'
	request['data']['feSkinName'] = 'skin-gray'
	request['data']['lat'] = '40.04504655364699'
	request['data']['lon'] = '116.3162245168386'
	request['data']['phoneTyep'] = 'iPhone'
	request['data']['province'] = '北京市'
	request['data']['city'] = '北京市'
	request['data']['area'] = '海淀区'
	request['data']['screenType'] = '1'
	request['data']['screenscale'] = '2'
	request['data']['token'] = '2_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM'