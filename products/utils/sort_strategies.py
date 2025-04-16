def sort_by_price(qs):
    return qs.order_by('price')

def sort_by_newest(qs):
    return qs.order_by('-id')
