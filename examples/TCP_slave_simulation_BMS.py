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
    pcs_port = int(args[2])
    curr_pcs_mode = 'current.mode.' + args[2] + '.txt'

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    try:
        #Create the server
        server = modbus_tcp.TcpServer(address='172.31.20.223', port=port)
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")

        server.start()

        slave_1 = server.add_slave(1)
        '아래 address no들은 모두 40000번을 0번으로 기준으로 만들어진 것으로, 추후 PMgrow 확인 후 변경 필요'
        slave_1.add_block('stop_server', cst.HOLDING_REGISTERS, 500, 1)
        slave_1.add_block('LGChem_BMS_1_BSC', cst.HOLDING_REGISTERS, 0, 50)
        slave_1.add_block('LGChem_BMS_1_Rack1', cst.HOLDING_REGISTERS, 50, 30)
        slave_1.add_block('LGChem_BMS_1_Rack2', cst.HOLDING_REGISTERS, 80, 30)
        slave_1.add_block('LGChem_BMS_1_Rack3', cst.HOLDING_REGISTERS, 110, 30)
        slave_1.add_block('LGChem_BMS_1_Rack4', cst.HOLDING_REGISTERS, 140, 30)

        slave_1.add_block('LGChem_BMS_1_module', cst.HOLDING_REGISTERS, 2000, 30)

        # PCS parameter 정의, 단위 : [kW]
        t = 0
        No_of_total_racks = 1
        PCS_P_ref = 500
        Bat_cap = 100
        SOC_before = 600
        Efficiency = 85

        # #Initialize BMS status
        slave_1.set_values('LGChem_BMS_1_BSC', 1, 0x0)
        slave_1.set_values('LGChem_BMS_1_BSC', 2, 0)        # BSC_Status
        slave_1.set_values('LGChem_BMS_1_BSC', 3, No_of_total_racks)    # BSC_information
        slave_1.set_values('LGChem_BMS_1_BSC', 4, No_of_total_racks)    # No_of_total_racks
        slave_1.set_values('LGChem_BMS_1_BSC', 5, 0)        # No_of (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 6, 0)        # No_of_warning_racks
        slave_1.set_values('LGChem_BMS_1_BSC', 7, 0)        # No_of_fault_racks
        slave_1.set_values('LGChem_BMS_1_BSC', 8, No_of_total_racks)        # No_of_DS_closed_racks
        slave_1.set_values('LGChem_BMS_1_BSC', 9, 0)        # No_of_racks_module_fan_on
        slave_1.set_values('LGChem_BMS_1_BSC', 10, 0)       # No_of_racks_Cell_balancing
        slave_1.set_values('LGChem_BMS_1_BSC', 11, 0)       # BSC_Warning_Code
        slave_1.set_values('LGChem_BMS_1_BSC', 12, 0)       # BSC_Fault_Code
        slave_1.set_values('LGChem_BMS_1_BSC', 13, 600)    # BSC_SOC (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 14, 600)    # BSC_SOH (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 15, 50)    # BSC_DC_Voltage (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 16, 100)    # BSC_DC_Current
        slave_1.set_values('LGChem_BMS_1_BSC', 17, 0)    # BSC_DC_Charge_Current_Limit
        slave_1.set_values('LGChem_BMS_1_BSC', 18, 0)    # BSC_DC_Discharge_Current_Limit
        slave_1.set_values('LGChem_BMS_1_BSC', 19, 0)    # BSC_DC_Charge_Power_Limit
        slave_1.set_values('LGChem_BMS_1_BSC', 20, 0)    # BSC_DC_Discharge_Power_Limit
        slave_1.set_values('LGChem_BMS_1_BSC', 21, 0)    # BSC_Max_Cell_Voltage (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 22, 0)    # BSC_Max_Cell_Location (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 23, 0)    # BSC_Min_Cell_Voltage (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 24, 0)    # BSC_Min_Cell_Voltage_Location (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 25, 0)    # BSC_Max_Module_Temperature (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 26, 0)    # BSC_Max_Module_Temperature_Location (online_racks)
        slave_1.set_values('LGChem_BMS_1_BSC', 27, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 28, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 29, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 30, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 31, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 32, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 33, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 34, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 35, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 36, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 37, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 38, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 39, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 40, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 41, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 42, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 43, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 44, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 45, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 46, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 47, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 48, 0)
        slave_1.set_values('LGChem_BMS_1_BSC', 49, 0)

        slave_1.set_values('LGChem_BMS_1_Rack1', 50, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 51, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 52, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 53, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 54, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 55, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 56, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 57, 0)   #Rack SOC
        slave_1.set_values('LGChem_BMS_1_Rack1', 58, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 59, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 60, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 61, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 62, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 63, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 64, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 65, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 66, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 67, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 68, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 69, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 70, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 71, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 72, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 73, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 74, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 75, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 76, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 77, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 78, 0)
        slave_1.set_values('LGChem_BMS_1_Rack1', 79, 0)

        slave_1.set_values('LGChem_BMS_1_Rack2', 80, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 81, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 82, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 83, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 84, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 85, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 86, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 87, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 88, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 89, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 90, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 91, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 92, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 93, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 94, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 95, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 96, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 97, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 98, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 99, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 100, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 101, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 102, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 103, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 104, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 105, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 106, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 107, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 108, 0)
        slave_1.set_values('LGChem_BMS_1_Rack2', 109, 0)

        slave_1.set_values('LGChem_BMS_1_Rack3', 110, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 111, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 112, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 113, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 114, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 115, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 116, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 117, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 118, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 119, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 120, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 121, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 122, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 123, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 124, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 125, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 126, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 127, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 128, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 129, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 130, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 131, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 132, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 133, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 134, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 135, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 136, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 137, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 138, 0)
        slave_1.set_values('LGChem_BMS_1_Rack3', 139, 0)

        slave_1.set_values('LGChem_BMS_1_module', 2000, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2001, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2002, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2003, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2004, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2005, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2006, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2007, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2008, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2009, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2010, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2011, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2012, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2013, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2014, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2015, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2016, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2017, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2018, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2019, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2020, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2021, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2022, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2023, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2024, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2025, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2026, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2027, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2028, 0)
        slave_1.set_values('LGChem_BMS_1_module', 2029, 0)

        while True:
            # PCS로부터 Pref를 받아옴
            c_mode = None
            PCS_P_ref = None
            try:
                f = open(curr_pcs_mode,'r')
                oneline = f.readline()
                c_mode = oneline.split(' ')[0]
                PCS_P_ref = float(oneline.split(' ')[1])
                print('mode: ' + c_mode + ', c_rate:' + str(PCS_P_ref))
                f.close()
            except:
                print('wrong info from :'+curr_pcs_mode)
                sleep(1)
                continue

            # Master로부터 server stop 명령 받기. (시뮬레이션이라서 편의상 추가)
            stop_cmd = slave_1.get_values('stop_server', 500, 1)
            if stop_cmd[0] == 100:
                break

            # Heartbeat
            Heartbeat = t%2

            # SOC 계산 로직
            if PCS_P_ref >= 32768:
		PCS_P_ref = PCS_P_ref - 65535 
	    SOC_del = -PCS_P_ref/Bat_cap/3600.0*Efficiency/100.0*100
            SOC_after = SOC_before + SOC_del
            SOC_before = SOC_after
            BSC_SOC = int(SOC_after)
	    print('PCS_P_ref = '+str(PCS_P_ref))
            print('SOC_del = '+str(SOC_del))
            print('SOC = '+str(SOC_after))
	    # DC 전압 전류 계산 로직
	    if BSC_SOC > 0 and BSC_SOC <= 150:
		BSC_DC_voltage = int(6000 + 1900.0/150.0*BSC_SOC)
	    elif BSC_SOC > 150 and BSC_SOC <= 850:
		BSC_DC_voltage = int(7900 + 600.0/700.0*(BSC_SOC-150))
	    elif BSC_SOC > 850 and BSC_SOC <= 1000:
		BSC_DC_voltage = int(8500 + 10*(BSC_SOC-850))
	    else:
		BSC_DC_voltage = 0
	    print('BSC_DC_voltage = '+str(BSC_DC_voltage))
	    # DC 전류 계산 로직
	    BSC_DC_current = (int(PCS_P_ref/BSC_DC_voltage*1000*10)+65535)%65535
	    print('BSC_DC_current = '+str(BSC_DC_current))

            # Update BMS status
            slave_1.set_values('LGChem_BMS_1_BSC', 1, Heartbeat)
            slave_1.set_values('LGChem_BMS_1_BSC', 13, BSC_SOC)
	    slave_1.set_values('LGChem_BMS_1_BSC', 15, BSC_DC_voltage)
	    slave_1.set_values('LGChem_BMS_1_BSC', 16, BSC_DC_current)

            # 시간 경과
            print('t = %d' % t)
            sleep(1)
            t = t + 1

    finally:
        server.stop()


if __name__ == "__main__":
    main(sys.argv)
