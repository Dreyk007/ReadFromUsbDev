#!/usr/bin/python3
# By Valentine Dreyk

import usb.core


def find_devs():
    devs = list(usb.core.find(find_all=True))

    for c, dev in enumerate(devs, start=1):
        name = '{}. {} - {} | {}:{}'.format(c, *list(get_dev_props(dev)))
        print(name)

    print()
    choice = int(input('Select device for read: '))
    dev = devs[choice - 1]

    return dev


def dev_read(dev, eaddr, max_packet_size):
    while True:
        try:
            resp = dev.read(eaddr, max_packet_size)
            yield resp
        except KeyboardInterrupt:
            break
        except:
            pass


def configure_dev(dev):
    ep = dev[0].interfaces()[0].endpoints()[0]
    interfaces = []
    for i in dev[0].interfaces():
        i = i.bInterfaceNumber
        interfaces.append(i)

    dev.reset()

    for i in interfaces:
        if dev.is_kernel_driver_active(i):
            dev.detach_kernel_driver(i)
            print('Dev driver detached!')

    dev.set_configuration()
    eaddr = ep.bEndpointAddress
    max_packet_size = ep.wMaxPacketSize

    return eaddr, max_packet_size


def get_dev_props(dev):
    try:
        yield dev.manufacturer
    except:
        yield None
    try:
        yield dev.product
    except:
        yield None
    try:
        yield hex(dev.idVendor)
    except:
        yield None
    try:
        yield hex(dev.idProduct)
    except:
        yield None


def main():
    dev = find_devs()
    eaddr, max_packet_size = configure_dev(dev)
    for c, resp in enumerate(dev_read(dev, eaddr, max_packet_size), start=1):
        resp = '{}: {}'.format(c, resp)
        print(resp)


if __name__ == '__main__':
    main()
