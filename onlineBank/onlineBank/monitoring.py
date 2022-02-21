from onlineBank.models import ip
import ipinfo

def recordAccess(request):
    requestIP = get_client_ip(request)
    alreadyGot = list(ip.objects.filter(ip=requestIP))
    for i in range(len(alreadyGot)):
        if alreadyGot[i].user == request.user:
            return
    ipDetails = resolveIP(requestIP)
    record = createRecord(requestIP, request.user, ipDetails)
    record.save()
    return

def createRecord(requestIP, user, ipDetails):
    record = ip()
    record.ip = requestIP
    if user.is_anonymous != True:
        record.user = user
    if 'country' in ipDetails:
        record.country = ipDetails['country']
    if 'region' in ipDetails:
        record.region = ipDetails['region']
    if 'city' in ipDetails:
        record.city = ipDetails['city']
    if 'postal' in ipDetails:
        record.postal = ipDetails['postal']
    if 'org' in ipDetails:
        record.isp = ipDetails['org']
    if 'latitude' in ipDetails:
        record.latitude = ipDetails['latitude']
    if 'longitude' in ipDetails:
        record.longitude = ipDetails['longitude']
    return record



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def resolveIP(ip):
    access_token = '6f4b955ad955d1'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    return details.all