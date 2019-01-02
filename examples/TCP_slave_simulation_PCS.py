#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

 This is distributed under GNU LGPL license, see license.txt
"""

import sys
import socket
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from time import sleep

def main(args):
    """main"""

    port = int(args[1])
    curr_pcs_mode = 'current.mode.' + args[1] + '.txt'
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    try:
        #Create the server
        server = modbus_tcp.TcpServer(port=port)
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")
        server.start()
        slave_1 = server.add_slave(1)
        slave_1.add_block('PCS_destin_1_Status', cst.HOLDING_REGISTERS, 0, 200)
        slave_1.add_block('PCS_destin_1_Ctrl&CMD', cst.HOLDING_REGISTERS, 3000, 70)
        slave_1.add_block('stop_server', cst.HOLDING_REGISTERS, 200, 1)
        # Default values
        # slave_id : 1
        # block_name : 0
        t = 0

        # PCS parameter 정의, 단위 : [kW]
        PCS_Prated = 500
	PCS_P = 0
	PCS_Pref = 0
	PCS_Qref = 0
        Bat_cap = 500
        SOC_init = 80
        SOC = [SOC_init]
        inv_efficiency = 0.98

        f = open('cumulative_charged_capacity.txt','r')
        cum_capacity_charged_before = int(float(f.read()))
	f.close()
	f = open('cumulative_discharged_capacity.txt','r')
        cum_capacity_discharged_before = int(float(f.read()))
	f.close()

        cum_capacity_charged_after = 0
        cum_capacity_charged_1kWh = int(cum_capacity_charged_before/10000)
        cum_capacity_charged_100mWh = int(cum_capacity_charged_before - cum_capacity_charged_1kWh*10000)
        cum_capacity_discharged_after = 0
        cum_capacity_discharged_1kWh = int(cum_capacity_discharged_before/10000)
        cum_capacity_discharged_100mWh = int(cum_capacity_discharged_before - cum_capacity_discharged_1kWh*10000)

        while True:
            # Master로부터 server stop 명령 받기. (시뮬레이션이라서 편의상 추가)
            stop_cmd = slave_1.get_values('stop_server', 200, 1)
            if stop_cmd[0] == 100:
                break

            # Get PCS Command
            PCS_CMD = slave_1.get_values('PCS_destin_1_Ctrl&CMD', 3000, 1)[0]
            PCS_Order_Source = slave_1.get_values('PCS_destin_1_Ctrl&CMD', 3043, 1)[0]
            PCS_Pref = slave_1.get_values('PCS_destin_1_Ctrl&CMD', 3064, 1)[0]
  	    print('PCS_Pref = '+str(PCS_Pref))
	    PCS_Qref = slave_1.get_values('PCS_destin_1_Ctrl&CMD', 3065, 1)[0] 
	    print('PCS_Qref = '+str(PCS_Qref))
	    
            # Calculate Cumulative charge/discharge capacity
            if PCS_Pref >= 32768:
                PCS_P = int((PCS_Pref-65535) * inv_efficiency + 65535)
                delta_cum_capacity_charged = abs((PCS_P-65535) * 1000/3600)
                print('PCS_P = '+str(PCS_P))
                cum_capacity_charged_after = cum_capacity_charged_before + delta_cum_capacity_charged
		if cum_capacity_charged_after >= 300000000:
		    cum_capacity_charged_after = 0
                cum_capacity_charged_1kWh = int(cum_capacity_charged_after/10000)
                cum_capacity_charged_100mWh = int(cum_capacity_charged_after - cum_capacity_charged_1kWh*10000)
                cum_capacity_charged_before = cum_capacity_charged_after
	        f = open('cumulative_charged_capacity.txt','w')
		f.write(str(cum_capacity_charged_before))
                f.close()	

            else:
                PCS_P = int(PCS_Pref*inv_efficiency)
                delta_cum_capacity_discharged = abs(PCS_P * 1000/3600)
                print('PCS_P = '+str(PCS_P))
                cum_capacity_discharged_after = cum_capacity_discharged_before + delta_cum_capacity_discharged
		if cum_capacity_discharged_after >= 300000000:
		    cum_capacity_discharged_after = 0
                cum_capacity_discharged_1kWh = int(cum_capacity_discharged_after/10000)
                cum_capacity_discharged_100mWh = int(cum_capacity_discharged_after - cum_capacity_discharged_1kWh*10000)
                cum_capacity_discharged_before = cum_capacity_discharged_after
		f = open('cumulative_discharged_capacity.txt','w')
                f.write(str(cum_capacity_discharged_before))
		f.close()
	    
            print('cum_capa_charged =' + str(cum_capacity_charged_before))
            print('cum_capa_charged_1kWh =' + str(cum_capacity_charged_1kWh))
            print('cum_capa_charged_100mWh ='+str(cum_capacity_charged_100mWh))
            print('cum_capa_discharged =' + str(cum_capacity_discharged_before))
            print('cum_capa_discharged_1kWh =' + str(cum_capacity_discharged_1kWh))
            print('cum_capa_discharged_100mWh =' + str(cum_capacity_discharged_100mWh))

            # Update PCS status
            slave_1.set_values('PCS_destin_1_Status', 5, cum_capacity_charged_1kWh)
            slave_1.set_values('PCS_destin_1_Status', 6, cum_capacity_charged_100mWh)
            slave_1.set_values('PCS_destin_1_Status', 7, cum_capacity_discharged_1kWh)
	    slave_1.set_values('PCS_destin_1_Status', 8, cum_capacity_discharged_100mWh)
            slave_1.set_values('PCS_destin_1_Status', 14, 57*1000) # PCS Freq, 1000배율
            slave_1.set_values('PCS_destin_1_Status', 15, 58*1000) # Grid Freq, 1000배율
            # slave_1.set_values('PCS_destin_1_Status', 20, 10)
            # slave_1.set_values('PCS_destin_1_Status', 21, 6)
            # slave_1.set_values('PCS_destin_1_Status', 22, 7)
            # slave_1.set_values('PCS_destin_1_Status', 23, 8)
            # slave_1.set_values('PCS_destin_1_Status', 24, 9)
            # slave_1.set_values('PCS_destin_1_Status', 29, 10)
            # slave_1.set_values('PCS_destin_1_Status', 30, 10)
            # slave_1.set_values('PCS_destin_1_Status', 31, 10)
            # slave_1.set_values('PCS_destin_1_Status', 32, 10)
            # slave_1.set_values('PCS_destin_1_Status', 33, 10)
            # slave_1.set_values('PCS_destin_1_Status', 34, 10)
            slave_1.set_values('PCS_destin_1_Status', 35, 59*10) # PCS Freq, 10배율
            # slave_1.set_values('PCS_destin_1_Status', 37, 17)
            # slave_3.set_values('PCS_destin_1_Status', 38, 18)
            # slave_1.set_values('PCS_destin_1_Status', 39, 19)
            # slave_1.set_values('PCS_destin_1_Status', 40, 20)
            # slave_1.set_values('PCS_destin_1_Status', 41, 21)
            # slave_1.set_values('PCS_destin_1_Status', 42, 22)
            slave_1.set_values('PCS_destin_1_Status', 44, 60*10) # Grid Freq, 10배율
            slave_1.set_values('PCS_destin_1_Status', 45, PCS_P)
            slave_1.set_values('PCS_destin_1_Status', 46, 0)
            # slave_1.set_values('PCS_destin_1_Status', 47, PF)
            # slave_1.set_values('PCS_destin_1_Status', 48, 27)
            # slave_1.set_values('PCS_destin_1_Status', 49, 28)
            # slave_1.set_values('PCS_destin_1_Status', 51, 29)
            # slave_1.set_values('PCS_destin_1_Status', 52, 30)
            # slave_1.set_values('PCS_destin_1_Status', 53, 31)
            # slave_1.set_values('PCS_destin_1_Status', 54, )
            # slave_1.set_values('PCS_destin_1_Status', 62, 33)
            # slave_1.set_values('PCS_destin_1_Status', 70, 4)
            # slave_1.set_values('PCS_destin_1_Status', 72, 35)
            # slave_1.set_values('PCS_destin_1_Status', 84, 36)
            # slave_1.set_values('PCS_destin_1_Status', 85, 37)
            # slave_1.set_values('PCS_destin_1_Status', 88, 38)
            # slave_1.set_values('PCS_destin_1_Status', 96, 39)
            # slave_1.set_values('PCS_destin_1_Status', 104, 40)

            print('p_ref:'+str(PCS_Pref))
            f = open(curr_pcs_mode,'w')
            c_mode='c'
            c_rate=float(PCS_Pref)
            f.write(c_mode + ' ' + str(c_rate))
            f.close()

            # 시간 경과
            print('t = %d' % t)
            sleep(1)
            t = t + 1

            # cmd = sys.stdin.readline()
            # args = cmd.split(' ')ls
            # if cmd.find('break') == 0:
            #     sys.stdout.write('bye-bye\r\n')
            #     break
            #
            # elif args[0] == 'add_slave':
            #     slave_id = int(args[1])
            #     server.add_slave(slave_id)
            #     sys.stdout.write('done: slave %d added\r\n' % slave_id)
            #
            # elif args[1] == 'add_block':
            #     slave_id = int(args[1])
            #     name = args[2]
            #     block_type = int(args[3])
            #     starting_address = int(args[4])
            #     length = int(args[5])
            #     slave = server.get_slave(slave_id)
            #     slave.add_block(name, block_type, starting_address, length)
            #     sys.stdout.write('done: block %s added\r\n' % name)
            #
            # elif args[0] == 'set_values':
            #     slave_id = int(args[1])
            #     name = args[3]
            #     address = int(args[3])
            #     values = []
            #     for val in args[4:]:
            #         values.append(int(val))
            #     slave = server.get_slave(slave_id)
            #     slave.set_values(name, address, values)
            #     values = slave.get_values(name, address, len(values))
            #     sys.stdout.write('done: values written: %s\r\n' % str(values))
            #
            # elif args[0] == 'get_values':
            #     slave_id = int(args[1])
            #     name = args[3]
            #     address = int(args[3])
            #     length = int(args[4])
            #     slave = server.get_slave(slave_id)
            #     values = slave.get_values(name, address, length)
            #     sys.stdout.write('done: values read: %s\r\n' % str(values))
            #
            # else:
            #     sys.stdout.write("unknown command %s\r\n" % args[0])

    finally:
        server.stop()


if __name__ == "__main__":
    main(sys.argv)
